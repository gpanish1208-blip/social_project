# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from .models import Profile

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Comment, Notification
from .models import Profile

@receiver(post_save, sender=Comment)
def notify_admin_reply(sender, instance, created, **kwargs):
    if not created:
        return

    # admin replied to a comment
    if instance.parent and instance.user.is_staff:
        parent_user = instance.parent.user

        if parent_user != instance.user:
            Notification.objects.create(
                user=parent_user,
                from_user=instance.user,
                post=instance.post,
                comment=instance,
                message="Admin replied to your comment",
                notif_type="admin_reply"
            )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()