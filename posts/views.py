from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Post, Profile, Comment, Report, Story
from .forms import RegisterForm, PostForm, ProfileForm, StoryForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from datetime import timedelta



# -------------------- USER AUTH --------------------

def register_view(request):
    """User registration"""
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()    # creates the user only (profile will be auto-created by signal)

            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')

    return render(request, 'posts/register.html', {'form': form})


def login_view(request):
    """User login"""
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "posts/login.html", {"form": form})


@login_required
def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


# -------------------- FEED & POSTS --------------------

@login_required
def home_feed(request):
    posts = Post.objects.all().order_by('-created_at')
    profiles = Profile.objects.select_related('user')

    # Active stories (last 24 hours)
    active_stories = Story.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=24)
    )

    # ✅ USERS WHO HAVE ACTIVE STORIES
    active_story_users = set(
        active_stories.values_list('user_id', flat=True)
    )

    return render(request, 'posts/home.html', {
        'posts': posts,
        'profiles': profiles,
        'active_story_users': active_story_users,  # ✅ PASS THIS
    })



@login_required
def create_post(request):
    """Create new post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Post uploaded successfully!")
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Handle comments
    if request.method == 'POST':
        content = request.POST.get('comment')
        if content:
            Comment.objects.create(user=request.user, post=post, content=content)
            return redirect('post_detail', pk=pk)

    # ✅ Fetch all reports for this post (put this HERE)
    reports = Report.objects.filter(post=post)

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'reports': reports,   # <- pass data to template
    })



@login_required
def delete_post(request, pk):
    """Delete post (only owner)"""
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        messages.error(request, "You can only delete your own posts.")
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('profile', username=request.user.username)

    return render(request, 'posts/delete_post.html', {'post': post})


@login_required
def like_post(request, pk):
    """Like or unlike a post"""
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count(),
        })
    return redirect('home')


# -------------------- COMMENTS --------------------

@login_required
def add_comment(request, pk):
    """Add comment (AJAX)"""
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(user=request.user, post=post, content=content)
        return JsonResponse({'comments_count': post.comments.count()})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_comment(request, comment_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid"}, status=400)

    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return JsonResponse({"error": "Forbidden"}, status=403)

    comment.delete()
    return JsonResponse({"status": "success"})



# -------------------- PROFILE --------------------

@login_required
def profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user_obj)

    posts = Post.objects.filter(user=user_obj).order_by('-created_at')

    return render(request, 'posts/profile.html', {
        'profile': profile,
        'posts': posts,
    })


@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'posts/edit_profile.html', {'form': form})



@login_required
def follow_user(request, username):
    """Follow/unfollow another user"""
    target_user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=target_user)

    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)

    return redirect('profile', username=username)


# -------------------- REPORTS --------------------

@login_required
def report_post(request, post_id):
    """Report a post"""
    if request.method == "POST":
        reason = request.POST.get("reason", "").strip()
        post = get_object_or_404(Post, pk=post_id)
        if reason:
            Report.objects.create(post=post, reported_by=request.user, reason=reason)
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error", "message": "Reason required"}, status=400)
    return JsonResponse({"status": "error"}, status=400)


# -------------------- CONTACT PAGE --------------------

def contact_view(request):
    """Contact form"""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        if name and email and message:
            messages.success(request, "Your message has been sent successfully!")
        else:
            messages.error(request, "Please fill out all fields.")
    return render(request, "posts/contact.html")


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')



@login_required
def notifications(request):
    reports = Report.objects.filter(reported_by=request.user, reply__isnull=False).order_by('-created_at')

    # Mark unread reports as read
    unread_reports = reports.filter(is_read=False)
    unread_reports.update(is_read=True)

    return render(request, 'posts/notifications.html', {'reports': reports})


@login_required
def upload_story(request):
    if request.method == 'POST':
        images = request.FILES.getlist('image')

        for img in images:
            Story.objects.create(
                user=request.user,
                image=img
            )

        return redirect('home')

    return render(request, 'posts/upload_story.html')







@login_required
def view_story(request, user_id):
    user = get_object_or_404(User, id=user_id)

    stories = Story.objects.filter(
        user=user,
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).order_by('created_at')

    # 👁️ ADD VIEW TRACKING
    for story in stories:
        if request.user != story.user:
            story.views.add(request.user)

    return render(request, 'posts/view_story.html', {
        'stories': stories,
        'story_user': user,
    })



@login_required
def delete_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    # Security check: only owner can delete
    if story.user != request.user:
        messages.error(request, "You are not allowed to delete this story.")
        return redirect('home')

    if request.method == "POST":
        story.delete()
        messages.success(request, "Story deleted successfully.")
        return redirect('home')

    return redirect('home')



# -------------------- FOLLOW --------------------

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = profile_user.profile

    posts = Post.objects.filter(user=profile_user)

    is_following = request.user.profile.following.filter(id=profile_user.id).exists()

    followers_count = profile.followers.count()
    following_count = profile.following.count()
    posts_count = posts.count()

    context = {
        "profile": profile,
        "profile_user": profile_user,
        "posts": posts,
        "is_following": is_following,
        "followers_count": followers_count,
        "following_count": following_count,
        "posts_count": posts_count,
    }
    return render(request, "posts/profile.html", context)


@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)

    my_profile = request.user.profile
    target_profile = target_user.profile

    if target_user in my_profile.following.all():
        my_profile.following.remove(target_user)
        target_profile.followers.remove(request.user)
    else:
        my_profile.following.add(target_user)
        target_profile.followers.add(request.user)

    return redirect("profile", username=username)


@login_required
def settings_view(request):
    return render(request, 'posts/settings.html')