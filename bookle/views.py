from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    context_dict = {}
    return render(request, 'bookle/home.html', context = context_dict)

def aboutus(request):
    context_dict = {}
    return render(request, 'bookle/aboutus.html', context = context_dict)

def leaderboard(request):
    context_dict = {}
    return render(request, 'bookle/leaderboard.html', context=context_dict)

def login(request):
    context_dict = {}
    return render(request, 'bookle/login.html', context=context_dict)

def pastpuzzles(request):
    context_dict = {}
    return render(request, 'bookle/pastpuzzles.html', context=context_dict)

def popular(request):
    context_dict = {}
    return render(request, 'bookle/popular.html', context=context_dict)

def difficult(request):
    context_dict = {}
    return render(request, 'bookle/difficult.html', context=context_dict)
