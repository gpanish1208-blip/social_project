from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Profile,Story
from django.contrib.auth.forms import AuthenticationForm

# ----------------------------
# User registration form
# ----------------------------

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': ' ',
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': ' ',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': ' ',
            'class': 'form-control'
        })




class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': ' ',
            'class': 'form-control'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': ' ',
            'class': 'form-control'
        })


# ----------------------------
# Post creation form

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'caption': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a caption...'
            }),
        }

# ----------------------------
# Comment form
# ----------------------------
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': 'Add a comment...'
            }),
        }

# ----------------------------
# Profile edit form
# ----------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class PostForm(forms.ModelForm):
    caption = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'rows': 3,
        'placeholder': 'Write a caption...'
    }))

    class Meta:
        model = Post
        fields = ['image', 'caption']


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image']
