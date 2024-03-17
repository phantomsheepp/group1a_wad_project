from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bookle.models import Comment
from bookle.forms import CommentForm
from bookle.models import Puzzle
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
        puzzle_id = 1 # Replace with your default puzzle ID

    puzzle = get_object_or_404(Puzzle, pk=puzzle_id)
    comments = Comment.objects.filter(puzzleID=puzzle).order_by('-commentID')

    if request.method == 'POST':
        form = CommentForm(request.POST, user=request.user)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.puzzleID = puzzle
            new_comment.rating = request.POST.get('rating')  # Get the rating from the form data
            new_comment.save()
    else:
        form = CommentForm(user=request.user)

    context = {
        'puzzle': puzzle,
        'comments': comments,
        'form': form,
    }

    return render(request, 'bookle/discussion.html', context)


