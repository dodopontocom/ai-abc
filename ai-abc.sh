#!/usr/bin/env bash

lang=$1
extra=${2:-}

echo "Gerando script Hello World em ${lang} com funcionalidade extra: ${extra}"

case ${lang} in
  "python")
    echo ${lang} ${extra} >> hello-world.py
    ;;
  "java")
    echo ${lang} ${extra} >> hello-world.java
    ;;
esac

echo "Script gerado com sucesso: hello-world.$lang"
