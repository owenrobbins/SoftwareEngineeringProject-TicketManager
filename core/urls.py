 # core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core' # Best practice to separate namespaces

urlpatterns = [
    # Maps each URL pattern to corresponding view
    # Custom Views
    path('', views.home, name='home'), # Root URL (Home)
    path('register/', views.register, name='register'), # Registration 
    path('tickets/', views.ticket_list, name='ticket_list'), # List of all tickets
    path('tickets/create/', views.create_ticket, name='create_ticket'), # Create Ticket
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket_detail'), # Details of the Ticket
    
    # Built in Django Views
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'), # Login (specifying the specific auth view)
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logged_out.html'), name='logout'), # Logout
]