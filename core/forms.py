from django import forms
from .models import Ticket

# Model view of the ticket form for the create button view
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'project', 'status', 'priority', 'assigned_to']