import os
import duolingo
import json
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response

from ..models.mango import Mango
from ..serializers import MangoSerializer, UserSerializer

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

lingo  = duolingo.Duolingo(USERNAME, PASSWORD)



# Create your views here.
class DuoLingo(APIView):
    authentication_classes=[]
    permission_classes=[]

    def post(self, request):
        """Index request"""
        
        source_language = request.data['source_language'] # 'es' or 'en'
        target_language = request.data['target_language'] # 'en' or 'la'
        username = request.data['username'] # 'Anjanasbabu' or 'BenJenkins8'

        # source_language = 'en'
        # target_language = 'la'
        # username = 'BenJenkins8'
        print(source_language)
        print(target_language)
        print(username)
        
        lingo.set_username(username)
        print(lingo.get_languages(abbreviations=True))

        skills = lingo.get_learned_skills(target_language)
        # print('skills', skills)
        
        words_lists = map(lambda skill: skill['words'], skills)

        # flatten them: https://stackoverflow.com/a/952952/3500171
        words = [item for sublist in words_lists for item in sublist]

        target_to_source_translations = lingo.get_translations(words, source=target_language, target=source_language)
        source_translation_lists = target_to_source_translations.values()
        source_translations = [item for sublist in source_translation_lists for item in sublist]

        dirty_source_to_target_translations = lingo.get_translations(source_translations, source=source_language, target=target_language)
        # remove the empty translations
        source_to_target_translations = filter(lambda item: item[1] != [], dirty_source_to_target_translations.items())
        data = json.dumps({ 'source_to_target_translations': dict(source_to_target_translations) })
        print(data)

        return Response(data)
