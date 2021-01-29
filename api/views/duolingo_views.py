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

# Pull personal USERNAME and PASSWORD from .env credentials
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Sign in to duolingo API
lingo  = duolingo.Duolingo(USERNAME, PASSWORD)
DELAY = 0.5

# Initialize engine used to pluralize words
engine = inflect.engine()

class DuoLingo(APIView):
    # disable authentication for this route
    authentication_classes=[]
    permission_classes=[]

    def post(self, request):
        """Index request"""

        # Extract username from incoming request and set it
        username = request.data['username'] # ex. 'Anjanasbabu' or 'BenJenkins8'
        lingo.set_username(username)

        # Delay to make sure username is set before continuing
        time.sleep(DELAY)

        # It seems I can only get translations for the current language, so extract the
        # ui_language - The language they are using in duolingo
        # target_language - the language currently being learned in duo lingo
        user_info = lingo.get_user_info()
        source_language = user_info['ui_language']
        target_language = lingo.get_abbreviation_of(user_info['learning_language_string'])

        print('username', username, 'source_language', source_language, 'target_language', target_language)

        skills = lingo.get_learned_skills(target_language)
        words_lists = map(lambda skill: skill['words'], skills)

        # flatten them: https://stackoverflow.com/a/952952/3500171
        all_target_words = [item for sublist in words_lists for item in sublist]

        target_to_source_translations = lingo.get_translations(all_target_words, source=target_language, target=source_language)
        source_translation_lists = target_to_source_translations.values()
        source_translations = [item for sublist in source_translation_lists for item in sublist]

        # TODO: Attempt to pluralize any words missing from duolingo
        if source_language == 'en' and target_language == 'la':
            for i in range(len(source_translations)):

                english_source_word = source_translations[i]
                print(english_source_word, '->', end='')
                try:
                    plural_english_source_word = engine.plural(english_source_word)
                except:
                    print("Unexpected error:", english_source_word)
                else:
                    source_translations.append(plural_english_source_word)

        dirty_source_to_target_translations = lingo.get_translations(source_translations, source=source_language, target=target_language)

        # Filter out any translations that include words I don't know yet
        for source_word, target_words in dirty_source_to_target_translations.items():
          dirty_source_to_target_translations[source_word] = list(filter(lambda target: target in all_target_words, target_words))

        # remove the empty translations
        source_to_target_translations = dict(filter(lambda item: item[1] != [], dirty_source_to_target_translations.items()))

        data = json.dumps({ 'source_to_target_translations': source_to_target_translations })

        return Response(data)
