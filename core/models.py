from django.db import models
from django.contrib.auth.models import User

# Space to create models

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='projects', null=True, blank=True) # If user deleted, allows the project to go unassigned
    
    def __str__(self):
        return self.name # shows project name in admin panel
    
class Ticket(models.Model):
    class Status(models.TextChoices): # Inner class for Status enum choices
        TO_DO = "TO-DO", "To-Do"
        In_PROGRESS = "IN_PROGRESS", "In Progress"
        FOR_REVIEW = "FOR_REVIEW", "For Review"
        DONE = "DONE", "Done"
    class Priority(models.TextChoices): # Inner class for priorty enum choices
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        
    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tickets")
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.TO_DO)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # If User deleted, sets the created_by and assigned_to to NULL / unassigned
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_tickets") 
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets")
    
    def __str__ (self):
        return self.title
    
class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__ (self):
        return self.text[:30] # Returns first 30 characters of the comment
    
class UserProfile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.username