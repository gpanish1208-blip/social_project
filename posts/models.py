from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_image = models.ImageField(upload_to='profile_images/', default='default.jpg')
    bio = models.TextField(blank=True)

    followers = models.ManyToManyField(User, related_name="followed_by", blank=True)
    following = models.ManyToManyField(User, related_name="follows", blank=True)
    def __str__(self):
        return self.user.username



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(blank=True, null=True)  # allow empty caption
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f'{self.user.username} Post'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Comment'
    
class Report(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    reason = models.TextField()
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.reported_by} on Post {self.post.id}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"

class Report(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reports")
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    reply = models.TextField(blank=True, null=True)  # admin reply
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # notification


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    image = models.ImageField(upload_to='stories/')
    created_at = models.DateTimeField(auto_now_add=True)

    views = models.ManyToManyField(
        User,
        related_name='viewed_stories',
        blank=True
    )

    @property
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=24)
