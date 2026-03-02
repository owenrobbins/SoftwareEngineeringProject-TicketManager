from django.contrib import admin
from .models import Project
from .models import Ticket
from .models import Comment
from .models import UserProfile

# Registering models here makes them visible and manageable in Django's built in 
# admin panel on /admin/. Without this the models exist within the database and 
# can be managed within terminal however cannot be accessed through admin UI.
# Django admin documents: https://docs.djangoproject.com/en/6.0/ref/contrib/admin/

admin.site.register(Project)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(UserProfile)