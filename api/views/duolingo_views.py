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

        target_vocab_dict = lingo.get_vocabulary(language_abbr=target_language)['vocab_overview']
        all_target_words = sorted(map(lambda target_vocab: target_vocab['normalized_string'], target_vocab_dict))

        # Get translations from duolingo
        target_to_source_translations = lingo.get_translations(all_target_words, source=target_language, target=source_language)

        # Build up translations from the source language into the target language
        source_to_target_translations = {}

        # Get versions of the translation without parenthesis
        def without_parenthesis(source_translation):
            paren_start = source_translation.index("(")
            paren_end = source_translation.index(")")
            removal_start = paren_start
            removal_end = paren_end

            space_removed = False
            if removal_start != 0:
                removal_start -= 1
                space_removed = True
            if not space_removed and space_removed != len(source_translation) - 1:
                removal_end += 1

            # source without parenthesis, text inside parenthesis, and a space touching parenthesis (if exists)
            source_without_parenthetical = source_translation[0:removal_start] + source_translation[removal_end + 1:]

            # source without parenthesis (but still containing the text inside the parenthesis)
            source_without_parenthesis = source_translation[0:paren_start] + source_translation[paren_start + 1:paren_end] + source_translation[paren_end + 1:]
            print(source_translation, "without parenthetical", source_without_parenthetical, "without parenthesis", source_without_parenthesis)
            return source_without_parenthetical, source_without_parenthesis

        # Get versions of the translation without /. Expand the / into the possible options
        # "he/she/it drinks" becomes ["he drinks", "she drinks", "it drinks"]
        def split_on_forward_slashes(source_translation):
            translations = []
            source_words = source_translation.split()

            # loop through each word
            for i, source_word in enumerate(source_words):

                # if the word has multiple options ex. he/she/it
                if "/" in source_word:
                    # create a list of the options ex. ["he", "she", "it"]
                    possibilities = source_word.split("/")
                    # print("source_translation", source_translation, "possibilities", possibilities)

                    # for each possibility
                    for possibility in possibilities:
                        # create a new translation with each individual option
                        new_words = source_words[0:i] + [possibility] + source_words[i + 1:]
                        rejoined_translation = " ".join(new_words)

                        # add it to the list of translations
                        translations.append(rejoined_translation)
                    # print(source_translation, translations)

            return translations

        # Add the translation to the source_to_target_translations object
        # Handle parenthesis and different options specificed by "/"s
        def add_target_to_source(source_translation, target):
            # If we have parenthesis in the term
            if "(" in source_translation and ")" in source_translation:
                # Get versions without parenthesis
                print(source_translation)
                source_without_parenthetical, source_without_parenthesis = without_parenthesis(source_translation)
                # Call this function on the versions without parenthesis
                add_target_to_source(source_without_parenthetical, target)
                add_target_to_source(source_without_parenthesis, target)
            elif "/" in source_translation:
                optional_translations = split_on_forward_slashes(source_translation)

                for optional_translation in optional_translations:
                    add_target_to_source(optional_translation, target)
            else:
              # If there aren't parenthesis in the source translation
              # Add the source_translation to the dictionary
              if source_translation not in source_to_target_translations:
                  source_to_target_translations[source_translation] = []

              if "(" in source_translation or ")" in source_translation:
                  print("Questionable:", source_translation)
              source_to_target_translations[source_translation].append(target)

        for target, source_translations in target_to_source_translations.items():
            for source_translation in source_translations:
                normalized_source_translation = re.sub('[\.\?\-]', '', source_translation.lower())
                add_target_to_source(normalized_source_translation, target)


        # print(source_to_target_translations)

        with open('target_to_source_translations.json', 'w', encoding='utf-8') as f:
            json.dump(target_to_source_translations, f, ensure_ascii=False, indent=4)

        with open('source_to_target_translations.json', 'w', encoding='utf-8') as f:
            json.dump(source_to_target_translations, f, ensure_ascii=False, indent=4)


        # Filter out any translations that include words I don't know yet
        for source_word, target_words in source_to_target_translations.items():
          source_to_target_translations[source_word] = list(filter(lambda target: target in all_target_words, target_words))

        # remove the empty translations
        source_to_target_translations = dict(filter(lambda item: item[1] != [], source_to_target_translations.items()))

        data = json.dumps({ 'source_to_target_translations': source_to_target_translations })

        return Response(data)
