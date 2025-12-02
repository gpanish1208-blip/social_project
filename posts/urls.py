from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home_feed, name='home'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Backup paths (different names to avoid conflicts)
    path('accounts/login/', views.login_view, name='login_alt'),
    path('accounts/logout/', views.logout_view, name='logout_alt'),
    path('accounts/register/', views.register_view, name='register_alt'),

    # Profile
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    # Posts
    path('create/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),

    # Report
    path('post/<int:post_id>/report/', views.report_post, name='report_post'),

    # Contact
    path('contact/', views.contact_view, name='contact'),

    path('notifications/', views.notifications, name='notifications'),

    path('story/upload/', views.upload_story, name='upload_story'),
    path('story/view/<int:user_id>/', views.view_story, name='view_story'),

    # Replace any unfollow URLs with toggle_follow
path("profile/<str:username>/follow/", views.toggle_follow, name="toggle_follow"),
    path("follow/<str:username>/", views.toggle_follow, name="toggle_follow"),




]
