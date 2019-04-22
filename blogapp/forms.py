from django import forms
from .models import article, author, Comment, category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateForm(forms.ModelForm):
    class Meta:
        model = article
        fields = [
            'title',
            'body',
            'image',
            'category',
        ]


class CreateRegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        ]


class CreateAuthorForm(forms.ModelForm):
    class Meta:
        model = author
        fields = [
            'profile_picture',
            'details'
        ]


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'name',
            'email',
            'post_comment',

        ]


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = [
            'name',
        ]
