from django.urls import path
from django.conf.urls import url 
from django.urls import include
from bookle import views

app_name = 'bookle'

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about_us, name='about_us'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('login/', views.login, name='login'),
    path('sign-up/', views.signup, name='signup'),
    path('home/daily-puzzle/', views.daily_puzzle, name='daily_puzzle'),
    path('home/past-puzzles/', views.past_puzzles, name='past_puzzles'),
    #I've written these but have no way of testing them at the moment as it needs the form logic! -sophie 
    path('login/view-account/', views.view_account, name='view_account'),
    path('login/view-account/edit-account/', views.edit_account, name='edit_account'),
    path('home/daily-puzzle/complete/', views.complete, name='complete'),
    path('home/daily-puzzle/complete/discussion/', views.discussion, name='discussion'),
]