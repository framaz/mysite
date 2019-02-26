from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

from django.urls import reverse
app_name="ticgame"
urlpatterns = [
    path('game',views.gameView , name='game'),
    path('gamesList',views.gamesList.as_view() , name='gamesList'),
    path('lout',views.fastLogout , name='lout'),
    path('startGame/<int:game>',views.gameSelect , name='startGame'),
    path('createGame',views.createGame , name='createGame'),
]
