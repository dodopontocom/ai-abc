#!/usr/bin/env bash

lang=$1
extra=${2:-}

echo "Gerando script Hello World em ${lang} com funcionalidade extra: ${extra}"

case ${lang} in
  "python")
    cat << EOF >> hello-world.py
#!/usr/bin/env python
print("Hello World")
EOF
    ;;
  "java")
    cat << EOF >> hello-world.java
Sua string aqui.
Outras linhas da sua string.
EOF
    ;;
esac

echo "Script gerado com sucesso: hello-world.$lang"
