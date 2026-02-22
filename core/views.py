# core/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
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

def is_admin(user):
    # Function to check if a user is an admin, and return result
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def delete_project(request, project_id): # Placeholder for an example admin request, with decorators to check login and admin privileges
    return