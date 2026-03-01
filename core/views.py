# core/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from core.models import Ticket
from .forms import TicketForm, CommentForm

def is_admin(user):
    # Helper Function to check if a user is an admin, and return result
    return user.is_staff

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
        
    return render(request, 'core/ticket_list.html', {'form': form, 'tickets': tickets})

def ticket_detail(request, pk):
    # View for clicking into the ticket, shows all the details and comments of the ticket
    # Also allows user to add new comments
    
    ticket = get_object_or_404(Ticket, pk=pk)
    comments = ticket.comments.select_related('author').order_by('created_at')
    
    if request.method == 'POST': # If user submitted a new comment
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.ticket = ticket
            new_comment.author = request.user
            new_comment.save()
            # Redirects back to the same page to avoid having to resubmit on the refresh
            return redirect('core:ticket_detail', pk=ticket.pk)
        
    else:
        comment_form = CommentForm()
    
    can_edit = request.user.is_authenticated and (request.user.is_staff or request.user == ticket.created_by)
    return render(request, 'core/ticket_detail.html', {
        'ticket': ticket,
        'comments': ticket.comments.all(),
        'comment_form': CommentForm(),
        'can_edit': can_edit        
    })
    
@login_required
def edit_ticket(request, pk):
    # View for editing ticket details, only accessible if logged in
    ticket = get_object_or_404(Ticket, pk=pk)
    # Checking for edit permissions
    if not (request.user.is_staff or request.user == ticket.created_by):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket) # Ties ticket form to existing ticket, updates rather than replace
        if form.is_valid():
            form.save()
            messages.success(request, "Ticket Updated Successfully")
            return redirect('core:ticket_detail', pk=ticket.pk) # Saves changes and redirects to see changes
    else:
        form = TicketForm(instance=ticket) # Fetches instance of form and prefills with information

    return render(request, 'core/ticket_edit.html', {'form': form, 'ticket': ticket})
        
# Delete Ticket View, only allowed for staff
@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == 'POST':
        # Delete the ticket and give feedback to user with message popup
        ticket.delete()
        messages.success(request, "Ticket deleted successfully.")
        return redirect('core:ticket_list')

    # If someone GETs the URL (shouldn't happen for modal flow), render a simple confirm page
    return render(request, 'core/ticket_confirm_delete.html', {'ticket': ticket})

@login_required
@user_passes_test(is_admin)
def delete_project(request, project_id): # Placeholder for deleting entire project, follows similar flow to delete ticket.
    return