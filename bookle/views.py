from django.shortcuts import render
from django.http import HttpResponse
from bookle.models import Score, Book
from django.views.generic import View
from bookle.helpers import get_book_names


def home(request):
    context_dict = {}
    return render(request, 'bookle/home.html', context = context_dict)

def about_us(request):
    context_dict = {}
    return render(request, 'bookle/about_us.html', context = context_dict)

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

def daily_puzzle(request):
    context_dict = {}
    context_dict['books'] = Book.objects.all().order_by('title')
    return render(request, 'bookle/daily_puzzle.html', context=context_dict)

class BookSuggestions(View):
    def get(self, request):
        if 'guess' in request.GET:
            guess = request.GET['guess']
        else:
            guess = ''
        
        books = get_book_names(max_results=5, starts_with=guess)
        
        
        return render(request, 'bookle/suggestions.html', {'books': books})

class CheckGuess(View):
    def get(self, request):
        if 'guess' in request.GET:
            guess = request.GET['guess']
        else:
            guess = ''

        return render(request, 'bookle/guess.html', {'title':guess})