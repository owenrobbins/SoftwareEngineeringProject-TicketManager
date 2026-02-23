# core/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from core.models import Ticket

def home(request):
    # Hompage for TicketLite
    return render(request, 'core/home.html')

def register(request):
    # User account registration screen
    if request.method == 'POST': # If the user is submitting the form
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:login') # Redirects the user to the login page after successfully registering user
    
    else: # If the user is just opening the Registration Form
        form = UserCreationForm()
    return render (request, 'core/register.html', {'form': form})

def ticket_list(request):
    # list of all active tickets for a project
    tickets = Ticket.objects.all()
    return render(request, 'core/ticket_list.html', {'tickets': tickets})

def is_admin(user):
    # Function to check if a user is an admin, and return result
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def delete_project(request, project_id): # Placeholder for an example admin request, with decorators to check login and admin privileges
    return