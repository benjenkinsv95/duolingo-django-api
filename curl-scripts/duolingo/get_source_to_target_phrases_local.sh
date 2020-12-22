#!/bin/bash

# source_language = request.data['source_language'] # 'es' or 'en'
# target_language = request.data['target_language'] # 'en' or 'la'
# username = request.data['username'] # 'Anjanasbabu' or 'BenJenkins8'

# SOURCE_LANGUAGE='en' TARGET_LANGUAGE='la' USERNAME='BenJenkins8' sh curl-scripts/duolingo/get_source_to_target_phrases.sh
# SOURCE_LANGUAGE='es' TARGET_LANGUAGE='en' USERNAME='Anjanasbabu' sh curl-scripts/duolingo/get_source_to_target_phrases.sh

curl "http://localhost:8000/source_to_target_phrases/" \
  --include \
  --request POST \
  --header "Content-Type: application/json" \
  --data '{
    "source_language": "'"${SOURCE_LANGUAGE}"'",
    "target_language": "'"${TARGET_LANGUAGE}"'",
    "username": "'"${USERNAME}"'"
  }'

echo
