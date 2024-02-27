#!/usr/bin/env python

# create commit message

import os
import subprocess
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_git_commit_message():

	git_changes = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
	message = model.generate_content('''Voce é um expert em criando mensagens para commites no github 
		para as mudanças relacionadas. Aqui está um diff das mudanças e preciso de uma mensagem para o commit (usar aproximadamente 30 palavras): ''' 
		+ str(git_changes))
	return message
	
if __name__ == '__main__':
    print(generate_git_commit_message().text)