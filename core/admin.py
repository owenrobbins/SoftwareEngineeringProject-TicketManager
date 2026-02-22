from django.contrib import admin
from .models import Project
from .models import Ticket
from .models import Comment
from .models import UserProfile

# Space to register models for use within Django admin ui

admin.site.register(Project)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(UserProfile)