import os
import duolingo
import json
import time
from rest_framework.views import APIView
import inflect
import re

from django.http import HttpResponse
from rest_framework.response import Response

from ..models.mango import Mango
from ..serializers import MangoSerializer, UserSerializer

# Pull personal USERNAME and PASSWORD from .env credentials
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Sign in to duolingo API
lingo  = duolingo.Duolingo(USERNAME, PASSWORD)
DELAY = 0.5

# Initialize engine used to pluralize words
engine = inflect.engine()

class DuoLingoAudio(APIView):
    # disable authentication for this route
    authentication_classes=[]
    permission_classes=[]

    def get(self, request):
        """Index request"""
        word = request.query_params.get('word')

        # Delay to make sure username is set before continuing
        time.sleep(DELAY)

        # It seems I can only get translations for the current language, so extract the
        # ui_language - The language they are using in duolingo
        # target_language - the language currently being learned in duo lingo
        user_info = lingo.get_user_info()
        source_language = user_info['ui_language']
        print('source_language', source_language)

        audio_url = lingo.get_audio_url(word)

        data = json.dumps({ 'audio_url': audio_url })

        return Response(data)
