from django.urls import path
from .views.mango_views import Mangos, MangoDetail
from .views.duolingo_views import DuoLingo
from .views.duolingo_audio_views import DuoLingoAudio
# DuoLingo
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword

urlpatterns = [
  	# Restful routing
    path('mangos/', Mangos.as_view(), name='mangos'),
    path('mangos/<int:pk>/', MangoDetail.as_view(), name='mango_detail'),
    path('source_to_target_phrases/', DuoLingo.as_view(), name='source_to_target_phrases'),
    path('word_to_audio/', DuoLingoAudio.as_view(), name='word_to_audio'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
