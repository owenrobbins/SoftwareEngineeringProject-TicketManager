from django.db import models
from django.contrib.auth.models import User

# Django models define the structure of the database tables
# Each class becomes a table with the sqlite db, each attribute becomes a column
# Django handles writing the sql itself, these classes handle the shape of the data
# Django models documentation: https://docs.djangoproject.com/en/6.0/intro/tutorial02/#creating-models
# Various field options to choose from: https://docs.djangoproject.com/en/6.0/ref/models/fields/

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True) # means this field isnt required within the forms
    created_at = models.DateTimeField(auto_now_add=True) #auto set on creation
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='projects', null=True, blank=True) # If user deleted, allows the project to go unassigned
    
    def __str__(self):
        return self.name # shows project name in admin panel
    
class Ticket(models.Model):
    
    # TextChoices is similar to an enum, provides options for a field
    # First value is stored in database, second is human-readable label

    class Status(models.TextChoices):
        TO_DO = "TO-DO", "To-Do"
        In_PROGRESS = "IN_PROGRESS", "In Progress"
        FOR_REVIEW = "FOR_REVIEW", "For Review"
        DONE = "DONE", "Done"
    class Priority(models.TextChoices):
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
    # Cascade here to delete any comments when the parent ticket is deleted
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__ (self):
        return self.text[:30] # Returns first 30 characters of the comment
    
class UserProfile (models.Model):
    # OneToOneField means that User can only have one profile, profile is deleted when the user is.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.username