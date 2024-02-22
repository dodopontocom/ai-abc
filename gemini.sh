#!/usr/bin/env bash

GEMINI_API_ENDPOINT="https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

PROMPT=$1
GEMINI_API_KEY=$2

CONTENT=$(echo -e " 
curl --silent -H 'Content-Type: application/json' \
  -d '{\"contents\":[{\"parts\":[{\"text\":\"${PROMPT}\"}]}]}' \
  -X POST ${GEMINI_API_ENDPOINT}?key=${GEMINI_API_KEY} \
  | jq -r '.candidates[0].content.parts[0].text'
")

eval ${CONTENT}
