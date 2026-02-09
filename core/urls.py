 # core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Maps the root URL to the home view
    path('', views.home, name='home'),
]

