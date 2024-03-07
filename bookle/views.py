from django.shortcuts import render
from django.http import HttpResponse
from bookle.models import Score
from bookle.models import Book


def home(request):
    context_dict = {}
    return render(request, 'bookle/home.html', context = context_dict)

def aboutus(request):
    context_dict = {}
    return render(request, 'bookle/aboutus.html', context = context_dict)

def leaderboard(request):
    # will need to see if this is correct, can't use until models are put in!
    #leaderboard_data = Score.objects.order_by('-guesses')[:5]
    context_dict = {}
    #context_dict['leaderboard_users'] = leaderboard_data
    return render(request, 'bookle/leaderboard.html', context=context_dict)

def login(request):
    context_dict = {}
    return render(request, 'bookle/login.html', context=context_dict)

def signup(request):
    context_dict = {}
    return render(request, 'bookle/signup.html', context=context_dict)

def daily_puzzle(request):
    context_dict = {}
    return render(request, 'bookle/daily_puzzle.html', context=context_dict)

