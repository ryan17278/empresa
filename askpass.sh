#!/bin/sh
# GIT_ASKPASS: entrega usuário/token vindos da env var, sem gravar nada.
case "$1" in
  Username*) echo "ryan17278" ;;
  *) echo "$GITHUB_TOKEN_EMPRESA" ;;
esac
