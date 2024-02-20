#!/usr/bin/env bash

string="falar 10 palavras sobre paulo leminski"
stringc=$(echo "$string" | urlencode)

curl ${GEMINI_API_ENDPOINT}/models/gemini-pro:generateContent?key=${GEMINI_API_KEY} \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[{
          "text": "$stringc"}]}]}' 2> /dev/null