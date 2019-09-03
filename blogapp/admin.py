from django.contrib import admin
from blogapp.models import Post, Comment, Profile

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)