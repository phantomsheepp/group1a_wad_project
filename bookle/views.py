from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from bookle.forms import RegisterForm, ProfileEditForm
from bookle.models import Score, Book
from django.views.generic import View
from bookle.helpers import get_book_names


def home(request):
    context_dict = {}
    return render(request, 'bookle/home.html', context = context_dict)

def about_us(request):
    context_dict = {}
    return render(request, 'bookle/about_us.html', context = context_dict)

@login_required
def leaderboard(request):
    # Uncomment the following lines when the models are ready
    # leaderboard_data = Score.objects.order_by('-guesses')[:5]
    # context = {'leaderboard_users': leaderboard_data}
    # return render(request, 'bookle/leaderboard.html', context)
    return render(request, 'bookle/leaderboard.html')

def login(request):
    context_dict = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                return redirect(reverse('bookle:home'))
            else:
                return HttpResponse("Your Bookle account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            context_dict['error_message'] = "Invalid login details supplied."
    return render(request, 'bookle/login.html', context_dict)
    
@login_required
def log_out(request):
    auth_logout(request)
    return redirect('bookle:home')

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                return render(request, 'bookle/signup.html', {'form': form, 'error': 'Username already exists'})
            user = form.save()
            # Authenticate the user
            user = authenticate(username=user.username, password=form.cleaned_data.get('password1'))
            # Log the user in
            auth_login(request, user)
            return redirect('bookle:home')
    else:
        form = RegisterForm()
    return render(request, 'bookle/sign_up.html', {'form': form})

@login_required
def profile(request, username=None):
    if username is None:
        username = request.user.username
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user.userprofile)
        if form.is_valid() and request.user.username == username:
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('bookle:profile', username=user.username)
    else:  # This is the GET request handler
        form = ProfileEditForm(instance=user.userprofile)
    return render(request, 'bookle/profile.html', {'form': form, 'user': user})

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

        if 'count' in request.GET:
            count = request.GET['count']
        else:
            count = 0

        finished = False

        """while guess_count < max_guesses:
        user_guess = input("Guess the book title: ")
        found, result, guessed_book = guess_book(user_guess)
        
        if not found:
            print(f"The book is not in our database. Did you mean '{', '.join(result)}'? Try again.")
            continue
        
        guess_count += 1
        if all(value == True for value in result.values()):
            print(f"Congratulations! You've guessed the book correctly in {guess_count} guesses.")
            print("Here are some information about the book:", guessed_book.description)
            break
        else:
            if guessed_book:
                print("Feedback on your guess:", result)
                print("Author:", guessed_book.author, "-", result["author"],
                      "Genre:", guessed_book.genre, "-", result["genre"],
                      "Release Year:", guessed_book.release_year, "-", result["release_year"],
                      "Country:", guessed_book.country, "-", result["country"])
"""
        if finished:
            return redirect()
        else:    
            return render(request, 'bookle/guess.html', {'title':guess})