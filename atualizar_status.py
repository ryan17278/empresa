#!/usr/bin/env python3
"""Atualiza só o status.json da empresa e dá push (GitHub Pages republica sozinho).

Uso:
  python3 atualizar_status.py novo_status.json        # substitui o status.json inteiro
  python3 atualizar_status.py --set bart.estado=trabalhando --set bart.tarefa="EP08"
  python3 atualizar_status.py --feed "Star|Ryan|texto"  # acrescenta uma entrada no feed
O token vem de GITHUB_TOKEN_EMPRESA (nunca é impresso nem gravado).
"""
import json, os, subprocess, sys, datetime, argparse
AQUI = os.path.dirname(os.path.abspath(__file__))
ST = os.path.join(AQUI, "status.json")
TZ = datetime.timezone(datetime.timedelta(hours=-3))

def main():
    if not os.environ.get("GITHUB_TOKEN_EMPRESA"):
        sys.exit("falta GITHUB_TOKEN_EMPRESA no ambiente")
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivo", nargs="?")
    ap.add_argument("--set", action="append", default=[])
    ap.add_argument("--feed", action="append", default=[])
    ap.add_argument("-m", "--msg", default="atualiza status.json")
    a = ap.parse_args()
    d = json.load(open(a.arquivo or ST, encoding="utf-8"))
    for s in a.set:
        k, v = s.split("=", 1); bot, campo = k.split(".", 1)
        d.setdefault(bot, {})[campo] = v
    agora = datetime.datetime.now(TZ)
    for f in a.feed:
        de, para, texto = f.split("|", 2)
        d.setdefault("feed", []).append({"de": de, "para": para, "texto": texto, "hora": agora.strftime("%d/%m %H:%M")})
    d["atualizado"] = agora.isoformat(timespec="seconds")
    json.dump(d, open(ST, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    env = dict(os.environ, GIT_ASKPASS=os.path.join(AQUI, "askpass.sh"), GIT_TERMINAL_PROMPT="0")
    g = lambda *c: subprocess.run(["git", "-C", AQUI, *c], env=env, check=True)
    g("add", "status.json")
    if subprocess.run(["git", "-C", AQUI, "diff", "--cached", "--quiet"]).returncode == 0:
        print("nada mudou"); return
    g("commit", "-q", "-m", a.msg)
    g("push", "-q", "origin", "main")
    print("status.json publicado:", d["atualizado"])

if __name__ == "__main__":
    main()
