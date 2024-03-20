from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bookle.models import Comment
from bookle.forms import CommentForm, ScoreForm
from bookle.models import Puzzle, Score
from bookle.forms import RegisterForm, ProfileEditForm
from django.http import JsonResponse

def home(request):
    context_dict = {}
    return render(request, 'bookle/home.html', context = context_dict)

def aboutus(request):
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

@login_required
def discussion(request, puzzle_id=None):
    if puzzle_id is None:
        puzzle_id = 1

    puzzle = get_object_or_404(Puzzle, pk=puzzle_id)
    has_rated = Score.objects.filter(userID=request.user, puzzleID=puzzle).exists()

    comment_form = CommentForm(user=request.user)
    rating_form = ScoreForm(user=request.user, puzzle=puzzle)

    if request.method == 'POST':
        if 'submit_comment' in request.POST:
            comment_form = CommentForm(request.POST, user=request.user)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.puzzleID = puzzle
                comment.save()
            rating_form = ScoreForm(user=request.user, puzzle=puzzle)
        elif 'submit_rating' in request.POST:
            rating_form = ScoreForm(request.POST, user=request.user, puzzle=puzzle)
            if rating_form.is_valid() and not has_rated:
                rating_form.save()
            comment_form = CommentForm(user=request.user)
    else:
        comment_form = CommentForm(user=request.user, puzzle=puzzle)
        rating_form = ScoreForm(user=request.user, puzzle=puzzle)

    comments = Comment.objects.filter(puzzleID=puzzle).order_by('-commentID')

    context = {
        'puzzle': puzzle,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'has_rated': has_rated,
    }

    return render(request, 'bookle/discussion.html', context)


