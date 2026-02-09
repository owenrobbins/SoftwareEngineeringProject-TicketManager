# core/views.py
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    # Renders in the hompage for TicketLite
    return render(request, 'core/home.html')