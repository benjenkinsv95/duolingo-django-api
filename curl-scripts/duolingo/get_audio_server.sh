#!/bin/bash

# WORD='combien' sh curl-scripts/duolingo/get_audio_server.sh

curl "https://duolingo-django-api.herokuapp.com/word_to_audio/?word=${WORD}" \
  --include \
  --request GET

echo
