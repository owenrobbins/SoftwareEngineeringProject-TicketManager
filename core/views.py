# core/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

def home(request):
    # Renders in the hompage for TicketLite
    return render(request, 'core/home.html')

def register(request):
    # Handles user registration using Django built in User Creation Form.
    if request.method == 'POST': # If the user is submitting the form
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:login') # Redirects the user to the login page after successfully registering user
    
    else: # If the user is just opening the Registration Form
        form = UserCreationForm()
    return render (request, 'core/register.html', {'form': form})