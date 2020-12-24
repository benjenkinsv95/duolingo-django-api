#!/bin/bash

# USERNAME='BenJenkins8' sh curl-scripts/duolingo/get_phrases_server.sh
# USERNAME='Anjanasbabu' sh curl-scripts/duolingo/get_phrases_server.sh
# USERNAME='abba-s' sh curl-scripts/duolingo/get_phrases_server.sh
# USERNAME='ID-007' sh curl-scripts/duolingo/get_phrases_server.sh
# USERNAME='Angelic12345' sh curl-scripts/duolingo/get_phrases_server.sh

curl "https://duolingo-django-api.herokuapp.com/source_to_target_phrases/" \
  --include \
  --request POST \
  --header "Content-Type: application/json" \
  --data '{
    "username": "'"${USERNAME}"'"
  }'

echo
