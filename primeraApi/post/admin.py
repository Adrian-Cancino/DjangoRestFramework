from django.contrib import admin

from .models import Post, Vote

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    model = Vote
