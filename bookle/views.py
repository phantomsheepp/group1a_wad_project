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

def past_puzzles(request):
    context_dict = {}
    return render(request, 'bookle/past_puzzles.html', context=context_dict)

def view_account(request):
    context_dict = {}
    return render(request, 'bookle/view_account.html', context=context_dict)

def edit_account(request):
    context_dict = {}
    return render(request, 'bookle/edit_account.html', context=context_dict)

def complete(request):
    context_dict = {}
    return render(request, 'bookle/complete.html', context=context_dict)

def discussion(request):
    context_dict = {}
    return render(request, 'bookle/discussion.html', context=context_dict)



