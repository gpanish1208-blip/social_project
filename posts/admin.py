from django.contrib import admin
from .models import Post, Comment, Profile, Report  # ✅ include Report

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username',)
    list_filter = ('user',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'created_at')
    search_fields = ('user__username', 'caption')
    list_filter = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'created_at')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'reported_by', 'reason', 'reply', 'created_at')
    search_fields = ('post__caption', 'reported_by__username', 'reason')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    fields = ('post', 'reported_by', 'reason', 'reply', 'created_at')
    readonly_fields = ('post', 'reported_by', 'reason', 'created_at')
