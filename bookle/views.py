from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.contrib.auth.models import User
from bookle.models import Score
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bookle.models import Comment
from bookle.forms import CommentForm, ScoreForm
from bookle.models import Puzzle, Score
from bookle.forms import RegisterForm, ProfileEditForm
from bookle.models import Score, Book, Puzzle, UserProfile
from django.views.generic import View
from bookle.helpers import get_book_names, get_guess_data, check_guess, get_target_book_data
from datetime import date, datetime
import json


def home(request):
    context_dict = {}
    return render(request, 'bookle/home.html', context = context_dict)

def about_us(request):
    context_dict = {}
    return render(request, 'bookle/about_us.html', context = context_dict)

@login_required
def leaderboard(request):
    puzzle = Puzzle.objects.filter(date=date.today())[0]
    todays_scores = Score.objects.filter(puzzleID=puzzle)
    leaderboard_data = todays_scores.order_by('guesses')[:5]
    context = {'leaderboard_guesses': leaderboard_data}
    return render(request, 'bookle/leaderboard.html', context)

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
    context_dict = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                return render(request, 'bookle/sign_up.html', {'form': form, 'error': 'Username already exists'})
            user = form.save()
            # Authenticate the user
            user = authenticate(username=user.username, password=form.cleaned_data.get('password1'))
            # Log the user in
            auth_login(request, user)
            return redirect('bookle:home')
        else:
            context_dict['error'] = "Sign up failed"
    else:
        form = RegisterForm()
    context_dict['form'] = form
    return render(request, 'bookle/sign_up.html', context=context_dict)

@login_required
def profile(request, username=None):
    user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.filter(user=user)[0]
    context_dict = {'user':user, 'userProfile':user_profile}
    return render(request, 'bookle/profile.html', context=context_dict)

@login_required
def edit_account(request, username):
    if request.user.username == username:
        user = get_object_or_404(User, username=username)
        if request.method == 'POST':
            form = ProfileEditForm(request.POST, request.FILES, instance=user.userprofile)
            if form.is_valid() and request.user.username == username:
                form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('bookle:profile', username=user.username)
        else:  # This is the GET request handler
            form = ProfileEditForm(instance=user.userprofile)
            return render(request, 'bookle/edit_account.html', {'form': form, 'user': user})
    else:
        return render(request, 'bookle/home.html', {})

@login_required
def discussion(request, puzzle_date="daily"):
    context_dict = {}

    if puzzle_date == "daily":
        puzzle_date = str(date.today())

    context_dict['puzzleDate'] = puzzle_date
    puzzle = get_object_or_404(Puzzle, date=puzzle_date)
    has_rated = False
    if not Score.objects.filter(userID=request.user, puzzleID=puzzle).exists():
        return redirect('bookle:daily_puzzle')

    s = Score.objects.get(userID=request.user, puzzleID=puzzle)
    has_rated = True if ((s.difficulty != None) or (s.popularity != None)) else False
    
    comment_form = CommentForm(user=request.user, puzzle=puzzle)
    rating_form = ScoreForm(instance=s)

    if request.method == 'POST':
        if 'submit_comment' in request.POST:
            comment_form = CommentForm(request.POST, user=request.user, puzzle=puzzle)
            if comment_form.is_valid():
                comment_form.save()
                comment_form = CommentForm(user=request.user, puzzle=puzzle)
                
        elif 'submit_rating' in request.POST:
            rating_form = ScoreForm(request.POST, instance=s)
            if rating_form.is_valid() and not has_rated:
                rating_form.save()
                return redirect('bookle:discussion', puzzle_date=puzzle_date)

    comments = Comment.objects.filter(puzzleID=puzzle).order_by('-commentID')

    context = {
        'puzzle': puzzle,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'has_rated': has_rated,
    }

    return render(request, 'bookle/discussion.html', context)

def daily_puzzle(request):
    if not Puzzle.objects.filter(date=date.today()):
        puzzleCount = len(Puzzle.objects.all())
        p = Puzzle.objects.create(puzzleID=puzzleCount+1, date=date.today(), isbn=Book.objects.all()[puzzleCount])
    else:
        p = Puzzle.objects.get(date=date.today())
        
    today = str(p.date)

    context_dict = {'puzzleDate':today}
    if request.user.is_authenticated:
        if Score.objects.filter(userID=request.user, puzzleID=p).exists():
            return complete(request, date=today)
        
    return render(request, 'bookle/daily_puzzle.html', context=context_dict)

def puzzle(request, date=None):
    context_dict = {}

    if Score.objects.filter(userID=request.user, puzzleID=puzzle).exists():
        return complete(request, date=date)

    try:
        puzzle_date = datetime.strptime(date, '%Y-%m-%d').date()
        context_dict['puzzleDate'] = str(puzzle_date)
    except:
        return redirect('bookle:home')
    
    get_object_or_404(Puzzle, date=puzzle_date)
    
    return render(request, 'bookle/daily_puzzle.html', context=context_dict)

def past_puzzles(request):

    pop_list = Puzzle.objects.order_by('-popularity')[:6]
    diff_list = Puzzle.objects.order_by('-difficulty')[:6]
    for p in pop_list:
        p.dateurl = str(p.date) 
    for p in diff_list:
        p.dateurl = str(p.date)   
    context_dict = {}
    context_dict['popular'] = pop_list
    context_dict['difficult'] = diff_list
    return render(request, 'bookle/past_puzzles.html', context=context_dict)

def complete(request, date="daily"):
    context_dict = {}
    return render(request, 'bookle/complete.html', context=context_dict)

class BookSuggestions(View):
    def get(self, request):
        if 'guess' in request.GET:
            guess = request.GET['guess']
        else:
            guess = ''
        
        books = get_book_names(max_results=5, starts_with=guess)
              
        return render(request, 'bookle/suggestions.html', {'books': books})

class DisplayGuess(View):
    def get(self, request):
        guess = request.GET.get('guess','')
        date = request.GET.get('date', '0000-0-0')

        context_dict = get_guess_data(guess, date)        

        return render(request, 'bookle/guess.html', context_dict)
        
class CheckGuess(View):
    def get(self, request):
        context_dict = {}
        
        guess = request.GET.get('guess','')
        date = request.GET.get('date', '0000-0-0')

        correct_guess, valid_guess = check_guess(guess, date)
        
        context_dict['correct_guess'] = (correct_guess)
        context_dict['valid_guess'] = (valid_guess)

        return HttpResponse(json.dumps(context_dict))
      
class SaveScore(View):
    def post(self, request):
        data = json.loads(request.body)
        guesses = data.get('count','')
        success = data.get('success', False)

        if User.objects.filter(username=data['user']):
            user = User.objects.get(username=data['user'])
            print("hey")
            if ('date' in data.keys()) and user.is_authenticated:
                puzzle_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
                puzzle = Puzzle.objects.get(date=puzzle_date)

                s = Score.objects.get_or_create(userID=user, puzzleID=puzzle)[0]
                s.success = success

                if success:
                    s.guesses = guesses
                s.save()

        return redirect('bookle:complete')
    
class GetBookData(View):
    def get(self, request):
        context_dict = {}

        puzzle_date_str = request.GET.get('date', '0000-0-0')
        if puzzle_date_str == "daily":
            puzzle_date_str = str(date.today())
        
        puzzle_date = datetime.strptime(puzzle_date_str, '%Y-%m-%d').date()
        puzzle = Puzzle.objects.get(date=puzzle_date)

        context_dict = get_target_book_data(puzzle)

        if request.user.is_authenticated:
            s = Score.objects.get(userID=request.user, puzzleID=puzzle)
            context_dict['success'] = s.success
            context_dict['guesses'] = s.guesses

        return HttpResponse(json.dumps(context_dict))