import os
import duolingo
import json
import time
from rest_framework.views import APIView
import inflect

from django.http import HttpResponse
from rest_framework.response import Response

from ..models.mango import Mango
from ..serializers import MangoSerializer, UserSerializer

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
lingo  = duolingo.Duolingo(USERNAME, PASSWORD)
DELAY = 1
# time.sleep(DELAY)



engine = inflect.engine()



# Create your views here.
class DuoLingo(APIView):
    authentication_classes=[]
    permission_classes=[]

    def post(self, request):
        """Index request"""
        
        username = request.data['username'] # 'Anjanasbabu' or 'BenJenkins8'
        lingo.set_username(username)
        time.sleep(DELAY)
        

        user_info = lingo.get_user_info()
        # source_language = request.data['source_language'] # 'es' or 'en'
        # target_language = request.data['target_language'] # 'en' or 'la'
        
        source_language = user_info['ui_language']
        target_language = lingo.get_abbreviation_of(user_info['learning_language_string'])

        # source_language = 'en'
        # target_language = 'la'
        # username = 'BenJenkins8'
        print(source_language)
        print(target_language)
        print(username)
        
        
        # print('bens', lingo.get_languages(abbreviations=True))
        # time.sleep(DELAY)
        
        # print('user_info', user_info)
        # print(user_info['ui_language'])
       
        # print()
        
        
        # 'ui_language': 'en'
        # 'tracking_properties': {'direction': 'fr<-en', 'took_placementtest': False, 'learning_language'
        # print('username', lingo.get_languages(abbreviations=True))
        # time.sleep(DELAY)

        skills = lingo.get_learned_skills(target_language)
        # time.sleep(DELAY)
        # print('skills', skills)
        
        words_lists = map(lambda skill: skill['words'], skills)
        # time.sleep(DELAY)

        # flatten them: https://stackoverflow.com/a/952952/3500171
        words = [item for sublist in words_lists for item in sublist]
        


        target_to_source_translations = lingo.get_translations(words, source=target_language, target=source_language)
        # time.sleep(DELAY)
        source_translation_lists = target_to_source_translations.values()
        source_translations = [item for sublist in source_translation_lists for item in sublist]
        
        # if source_language == 'en':
        #     for i in range(len(source_translations)):
                
        #         english_source_word = source_translations[i]
        #         print(english_source_word, '->', end='')
        #         try:
        #             plural_english_source_word = engine.plural(english_source_word)
        #         except:
        #             print("Unexpected error:", english_source_word)
        #         else:
        #             source_translations.append(plural_english_source_word)
                
               

        dirty_source_to_target_translations = lingo.get_translations(source_translations, source=source_language, target=target_language)
        # time.sleep(DELAY)
        # remove the empty translations
        source_to_target_translations = filter(lambda item: item[1] != [], dirty_source_to_target_translations.items())
        data = json.dumps({ 'source_to_target_translations': dict(source_to_target_translations) })
        print(data)

        return Response(data)
