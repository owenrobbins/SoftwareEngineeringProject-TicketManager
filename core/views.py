# core/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from core.models import Ticket
from .forms import TicketForm

def home(request):
    # Hompage for TicketLite
    form = TicketForm()
    return render(request, 'core/home.html', {'form': form})

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

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False) # Waits to commit new ticket so the creator can be done here
            ticket.created_by = request.user
            ticket.save()
            # Redirects after successful creation of ticket
            return redirect('core:ticket_list')
        else:
            # Form invalid - fall back and try rendering ticket-list with errors
            tickets = Ticket.objects.all() if request.user.is_authenticated else []
            return render(request, 'core/ticket_list.html', {'tickets': tickets, 'form': form})

    # If someone manages to get tickets/create just send back to tickets 
    return redirect('core:ticket_list')

def ticket_list(request):
    # list of all active tickets for a project, only shows list if logged in
    form = TicketForm()
    if request.user.is_authenticated:
        tickets = Ticket.objects.all()
    else:
        tickets = []
        
    return render(request, 'core/ticket_list.html', {'tickets': tickets, 'form': form})

def is_admin(user):
    # Function to check if a user is an admin, and return result
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def delete_project(request, project_id): # Placeholder for an example admin request, with decorators to check login and admin privileges
    return