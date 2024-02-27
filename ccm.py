#!/usr/bin/env python

# create commit message

import sys, os
import subprocess
import google.generativeai as genai

if len(sys.argv) > 1:
      key = sys.argv[1]
else:
      key = os.getenv("GEMINI_API_KEY")
      if key is None:
             print(f"Erro: A variável de ambiente GEMINI_API_KEY não está definida.")
             sys.exit(1)
            
genai.configure(api_key=(key))
model = genai.GenerativeModel('gemini-pro')

def generate_git_commit_message():
	git_changes = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
	message = model.generate_content('''Voce é um expert em criando mensagens para commites no github 
		para as mudanças relacionadas. Aqui está um diff das mudanças e preciso de uma mensagem para
		o commit (usar aproximadamente 30 palavras e usar frases impessoais): ''' 
		+ str(git_changes))
	return message
	
if __name__ == '__main__':
    print(generate_git_commit_message().text)