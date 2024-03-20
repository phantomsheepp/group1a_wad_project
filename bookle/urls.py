from django.urls import path
from django.conf.urls import url 
from django.urls import include
from bookle import views

app_name = 'bookle'

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about_us, name='about_us'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('past-puzzles/', views.past_puzzles, name='past_puzzles'),

    # Login and Sign Up
    path('login/', views.login, name='login'),
    path('log-out/', views.log_out, name='log_out'),
    path('sign-up/', views.sign_up, name='sign_up'),

    # Profile pages
    path('user/<str:username>/', views.profile, name='profile'),
    path('user/<str:username>/edit/', views.edit_account, name='edit_account'),
    
    # Puzzle pages
    path('puzzle/daily/', views.daily_puzzle, name='daily_puzzle'),
    path('puzzle/daily/complete/', views.Complete.as_view(), name='complete'),
    path('puzzle/daily/complete/discussion/', views.discussion, name='discussion'),
    
    # Views used for AJAX
    path('suggestions/', views.BookSuggestions.as_view(), name='suggestions'),
    path('check-guess/', views.CheckGuess.as_view(), name="check_guess"),
    path('display-guess/', views.DisplayGuess.as_view(), name="display_guess"),
    path('save-score/', views.SaveScore.as_view(), name="save_score"),
]