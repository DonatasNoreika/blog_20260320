from django import forms
from .models import CustomUser, Comment
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password1']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']