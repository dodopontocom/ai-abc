#!/usr/bin/env bash

lang=$1
extra=${1:-}

echo "Gerando script Hello World em ${lang} com funcionalidade extra: ${extra}"

case ${lang} in
  "python")
    echo "```python
    print(\'Hello World!\')

    # Funcionalidade extra
    if '${extra}' == 'data':
      print(\'Data atual:\', date)
    ```
    " > hello_world.py
    ;;
  "java")
    echo "```java
    public class HelloWorld {
      public static void main(String[] args) {
        System.out.println(\""Hello World!\");

        // Funcionalidade extra
        if (\"$extra\".equals(\"data\")) {
          System.out.println(\"Data atual: \" + java.time.LocalDate.now());
        }
      }
    }
    ```" > hello_world.java
    ;;
esac

echo "Script gerado com sucesso: hello_world.$lang"
