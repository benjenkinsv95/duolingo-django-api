#!/bin/bash

# USERNAME='BenJenkins8' sh curl-scripts/duolingo/get_phrases_local.sh
# USERNAME='Anjanasbabu' sh curl-scripts/duolingo/get_phrases_local.sh
# USERNAME='abba-s' sh curl-scripts/duolingo/get_phrases_local.sh
# USERNAME='ID-007' sh curl-scripts/duolingo/get_phrases_local.sh
# USERNAME='Angelic12345' sh curl-scripts/duolingo/get_phrases_local.sh

curl "http://localhost:8000/source_to_target_phrases/" \
  --include \
  --request POST \
  --header "Content-Type: application/json" \
  --data '{
    "username": "'"${USERNAME}"'"
  }'

echo
