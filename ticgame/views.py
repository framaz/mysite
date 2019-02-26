from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from . import forms
from django.contrib.auth.models import User
from django.urls import reverse
from django.core import exceptions
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.db.models import Q
import random
from .models import Game
@login_required
def gameView(request):
    return HttpResponse("stab")
    
def fastLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse("ticgame:sss"))
class gamesList(ListView):
    model=Game
    template_name='ticgame/games_list.html'
    def get_queryset(self):
        print(super().get_queryset().filter(is_ended=False),"azaza")
        return super().get_queryset().filter(is_ended=False)
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        counter = 0
        return context
@login_required
def gameSelect(request,game):
    curGame = get_object_or_404(Game, pk=game, is_ended=False)
    random.seed()
    if(random.choice([True,False]) == True):
        curGame.x_user=request.user
        curGame.o_user=curGame.hoster
    else:
        curGame.o_user=request.user
        curGame.x_user=curGame.hoster
    if(curGame.o_user == curGame.x_user):
        return HttpResponseNotFound('No game found')
    curGame.save()
    return redirect('ticgame:game')
    
@login_required
def createGame(request):
    if Game.objects.all().filter(Q(is_ended=False),Q(x_user=request.user)|Q(o_user=request.user)).count()==0:
        newGame = Game(hoster=request.user)
        newGame.save()
    return redirect('ticgame:game')
    
    
    