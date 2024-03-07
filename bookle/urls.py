from django.urls import path
from django.conf.urls import url 
from django.urls import include
from bookle import views

app_name = 'bookle'

urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('bookle/home/daily-puzzle/', views.daily_puzzle, name='daily_puzzle'),
]