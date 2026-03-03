 # core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Separating namespace so that URL's dont clash
# URLs are then referenced as 'core/...' 
# URL documentation: https://docs.djangoproject.com/en/6.0/intro/tutorial03/#namespacing-url-names

app_name = 'core' 


urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/<int:pk>/edit/', views.edit_ticket, name='edit_ticket'),
    path('tickets/<int:pk>/delete/', views.delete_ticket, name='delete_ticket'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create', views.create_project, name='create_project'),
    path('projects/<int:pk>', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit', views.edit_project, name='edit_project'),
    path('projects/<int:pk>/delete', views.delete_project, name='delete_project'),
    
    # Django's built in authorisation views rather than writing myself. 
    # Auth documentation: https://docs.djangoproject.com/en/6.0/topics/auth/
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logged_out.html'), name='logout'),
]