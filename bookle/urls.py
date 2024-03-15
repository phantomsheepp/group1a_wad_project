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
    path('log-out/', views.log_out, name='log_out'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/', views.profile, name='profile'),
    path('home/daily-puzzle/', views.daily_puzzle, name='daily_puzzle'),
    path('home/past-puzzles/', views.past_puzzles, name='past_puzzles'),
    #I've written these but have no way of testing them at the moment as it needs the form logic! -sophie 
    path('login/view-account/', views.view_account, name='view_account'),
    path('login/view-account/edit-account/', views.edit_account, name='edit_account'),
    path('home/daily-puzzle/complete/', views.complete, name='complete'),
    path('home/daily-puzzle/complete/discussion/', views.discussion, name='discussion'),
    
    # Views used for AJAX
    path('suggestions/', views.BookSuggestions.as_view(), name='suggestions'),
    path('check-guess/', views.CheckGuess.as_view(), name="check_guess"),
]