from django.urls import path
from django.conf.urls import url 
from django.urls import include
from bookle import views

app_name = 'bookle'

urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus/', views.aboutus, name='aboutus'),
]