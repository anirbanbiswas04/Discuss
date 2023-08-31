from django.contrib import admin

from .models import Story, Vote, Comment

admin.site.register(Story)
admin.site.register(Vote)
admin.site.register(Comment)