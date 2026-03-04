# core/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from core.models import Project, Ticket, UserProfile, Comment
from .forms import TicketForm, CommentForm, ProjectForm, UserProfileForm

def is_admin(user):
    # Helper Function to check if a user is an admin, and return result
    return user.is_staff

def landing(request):
    # Root URL entry point, logged in users get pushed straight to the dashboard, avoiding the login / logout page 
    if request.user.is_authenticated:
        return redirect('core:home')
    return render(request, 'core/landing.html')

@login_required
def home(request):
    # Hompage for TicketLite, shows quick actions and stats. 
    # @login_required measn that users get redirected to LOGIN_URL within settings
    
    # Global Stats
    total = Ticket.objects.count()
    projects_count = Project.objects.count()
    
    # Personally Assigned Stats (stats for tickets that are assigned to the user)
    todo_assigned_count = Ticket.objects.filter(status='TO-DO', assigned_to=request.user).count()
    in_progress_assigned_count = Ticket.objects.filter(status='IN_PROGRESS', assigned_to=request.user).count()
    for_review_assigned_count = Ticket.objects.filter(status='FOR_REVIEW', assigned_to=request.user).count()
    done_assigned_count = Ticket.objects.filter(status='DONE', assigned_to=request.user).count()
    assigned_to_me_count = Ticket.objects.filter(assigned_to=request.user).count()

    # Personall Assigned Ticket Lists (stats for tickets that are assigned to the user, most recent first)
    recent = Ticket.objects.filter(assigned_to=request.user).order_by('-created_at')[:6]
    todo_assigned = Ticket.objects.filter(status='TO-DO', assigned_to=request.user).order_by('-created_at')
    in_progress_assigned = Ticket.objects.filter(status='IN_PROGRESS', assigned_to=request.user).order_by('-created_at')
    for_review_assigned = Ticket.objects.filter(status='FOR_REVIEW', assigned_to=request.user).order_by('-created_at')
    done_assigned = Ticket.objects.filter(status='DONE', assigned_to=request.user).order_by('-created_at')

    # Combining all context stats into one dict to pass into render
    context = {
        'stats': {
            'total_tickets': total,
            'todo_assigned_count': todo_assigned_count,
            'in_progress_assigned_count': in_progress_assigned_count,
            'for_review_assigned_count': for_review_assigned_count,
            'done_assigned_count': done_assigned_count,
            'assigned_to_me_count': assigned_to_me_count,
            'projects': projects_count,
        },
        'recent_tickets': recent,
        'todo_assigned': todo_assigned,
        'in_progress_assigned': in_progress_assigned,
        'for_review_assigned': for_review_assigned,
        'done_assigned': done_assigned,
        'ticket_form': TicketForm(),   # For create modal form
    }
    return render(request, 'core/home.html', context)

def register(request):
    # Uses Django's build in UserCreationForm rather than writing manually.
    # On success, the user gets redirected to log-in rather than automatically logging in
    if request.method == 'POST': # If the user is submitting the form
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            return redirect('core:login')
    
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
            messages.success(request, "Ticket created successfully. ")
            # Redirects after successful creation of ticket
            return redirect('core:ticket_list')
        else:
            # Form invalid - fall back and try rendering ticket-list with errors to show validation to the user
            tickets = Ticket.objects.all() if request.user.is_authenticated else []
            return render(request, 'core/ticket_list.html', {
                'tickets': tickets, 
                'ticket_form': form,
                'show_modal': True
            })

    # If someone manages to get tickets/create just send back to tickets 
    return redirect('core:ticket_list')

@login_required
def ticket_list(request):
    # list of all active tickets for a project, only shows list if logged in
    form = TicketForm()
    if request.user.is_authenticated:
        tickets = Ticket.objects.all()
    else:
        tickets = []
        
    return render(request, 'core/ticket_list.html', {'ticket_form': TicketForm(), 'tickets': tickets})

@login_required
def ticket_detail(request, pk):
    # View for clicking into the ticket, shows all the details and comments of the ticket
    # get_object_or_404 fteches the ticket id, if it doesnt exist it displays a simple 404 page.
    
    ticket = get_object_or_404(Ticket, pk=pk)
    comments = ticket.comments.select_related('author').order_by('created_at')
    
    if request.method == 'POST': # If user submitted a new comment
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.ticket = ticket
            new_comment.author = request.user
            new_comment.save()
            # Redirects back to the same page to avoid comment resubmitting on the refresh
            return redirect('core:ticket_detail', pk=ticket.pk)
        
    else:
        comment_form = CommentForm()
    
    can_edit = request.user.is_authenticated and (request.user.is_staff or request.user == ticket.created_by)
    
    return render(request, 'core/ticket_detail.html', {
        'ticket': ticket,
        'comments': ticket.comments.all(),
        'comment_form': CommentForm(),
        'can_edit': can_edit,    
        'ticket_form': TicketForm(),   
    })
    
@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    # Only an admin or author of the comment can edit
    if not (request.user.is_staff or request.user.is_superuser or request.user == comment.author):
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "comment successfully updated ")
            return redirect('core:ticket_detail', pk=comment.ticket.pk)
    
    else: 
        form = CommentForm(instance=comment)
        
    return render(request, 'core/comment_edit.html', {
        'form': form,
        'comment': comment,
        'ticket_form': TicketForm(),
    })
    
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def delete_comment(request, pk):
    from .models import Comment
    comment = get_object_or_404(Comment, pk=pk)
    ticket_pk = comment.ticket.pk 
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment Succesfully Deleted")
        return redirect('core:ticket_detail', pk=ticket_pk)
    
    # Fallback if someone goes to the URL directly 
    return redirect('core:ticket_detail', pk=ticket_pk)
    
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

    return render(request, 'core/ticket_edit.html', {
        'form': form,
        'ticket': ticket,
        'ticket_form': TicketForm(),
        })
        
@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_ticket(request, pk):
    # Restricted the view to staff only through @user_passes_test
    # Deleting is handled via POST from a confirmation modal pop-up to avoid accidental deletion through links
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == 'POST':
        # Delete the ticket and give feedback to user with message popup
        ticket.delete()
        messages.success(request, "Ticket deleted successfully.")
        return redirect('core:ticket_list')

    # If someone GETs the URL (shouldn't happen for modal flow), render a simple confirm page
    return render(request, 'core/ticket_confirm_delete.html', {
        'ticket': ticket,
        'ticket_form': TicketForm()        
    })

@login_required
def project_list(request):
    # Shows a list of all projects
    projects = Project.objects.all().order_by('name')
    return render(request, 'core/project_list.html', {
        'projects': projects,
        'project_form': ProjectForm(),
        'ticket_form': TicketForm(), 
        })

@login_required
def project_detail(request, pk):
    # Shows a page displaying a single project and all tickets assigned to it
    # Uses select_related to fetch the data associated with the owner
    # Queryset Django Documentation: https://docs.djangoproject.com/en/6.0/ref/models/querysets/
    project = get_object_or_404(Project, pk=pk)
    tickets = project.tickets.select_related('assigned_to', 'created_by').order_by('-created_at')

    can_edit = request.user.is_staff or request.user == project.owner
    
    return render(request, 'core/project_detail.html', {
        'project': project,
        'tickets': tickets,
        'can_edit': can_edit,
        'ticket_form': TicketForm(),
    })

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        projects = Project.objects.all().order_by('name')
        if form.is_valid():
            project = form.save(commit=False) # Holds before saving so we can attach the project owner here
            project.owner = request.user
            project.save()
            messages.success(request, "Project created successfully. ")
            return redirect('core:project_list')
            
        return render(request, 'core/project_list.html', {
            'projects':  projects,
            'project_form': form,
            'ticket_form': TicketForm(),
            'show_modal': True # Re-opens the modal so that potential errors are visible
        })
    return redirect('core:project_list')
            
@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    #Only staff or project owner can edit
    if not (request.user.is_staff or request.user == project.owner):
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project Updated Successfully.")
            return redirect('core:project_detail', pk=project.pk)
        
    else:
        form = ProjectForm(instance=project)
            
    return render(request, 'core/project_edit.html', {
        'form': form, 
        'project': project,
        'ticket_form': TicketForm(),
        })
    
@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_project(request, pk):
    # Staff only
    # Follows same POST confirmation as delete_ticket
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully. ")
        return redirect('core:project_list')
    
    return redirect(render, 'core/project_confirm_delete.html', 
        {'project': project,
         'ticket_form': TicketForm()
    })
    
@login_required
def profile_view(request, pk):
    #Shows the user their profile page, of whoever is logged in
    
    profile_user = get_object_or_404(User, pk=pk)
    profile, _ = UserProfile.objects.get_or_create(user=profile_user) # uses 'or create' to handle any users created within admin tab
    can_edit = (request.user.is_staff or request.user.is_superuser) or request.user == profile_user
    
    return render(request, 'core/profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'can_edit': can_edit,
        'ticket_form': TicketForm()
    })
    
@login_required
def edit_profile(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    profile, _ = UserProfile.objects.get_or_create(user=profile_user)
    
    # Only the user themselves or an admin can edit
    if not (request.user.is_staff or request.user == profile_user):
        return HttpResponseForbidden
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated Profile. ")
            return redirect('core:profile_view', pk=profile_user.pk)
    
    else:
        form = UserProfileForm(instance=profile)
        
    return render(request, 'core/profile_edit.html', {
        'form': form,
        'profile_user': profile_user,
        'ticket_form': TicketForm()
    })
    
@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_user(request, pk):
    # Admin only, deletes the user account permanently 
    profile_user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        profile_user.delete()
        messages.success(request, f"User {profile_user.username} deleted. ")
        return redirect('core:home')
    
    return render(request, 'core/profile_confirm_delete.html', {
        'profile_user': profile_user,
        'ticket_form': TicketForm()
    })
    
@login_required
def user_list(request):
    users = User.objects.select_related('userprofile').order_by('username')
    return render(request, 'core/user_list.html', {
        'users': users,
        'is_privileged': request.user.is_staff or request.user.is_superuser,
        'ticket_form': TicketForm(), 
    })