from django import forms
from .models import Ticket, Comment, Project

# Model forms can create a form directly from the fields of a model class
# Can define what fields to include and customise how they appear 
# Keeping form logic separate from the views and templates
# Model Forms Documentation: https://docs.djangoproject.com/en/6.0/ref/forms/models/#

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'project', 'status', 'priority', 'assigned_to']
        
        # Widgets for control over what the HTML renders for each model field
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ticket Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'What is this ticket about?'
            }),
            'project': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text'] # Only the text field as ticket and author are set in the view
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add a comment...'
            }),
        }
        labels = {
            'text': 'Comment'
        }
    
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name','description']
        # Owner is set by default in the view, not chosen by the user
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project Name'
            }),
            
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What is this project about?'
            })
        }