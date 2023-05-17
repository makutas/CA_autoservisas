from .models import OrderListComment
from django import forms
from .models import Profile
from django.contrib.auth.models import User


class OrderListCommentForm(forms.ModelForm):
    class Meta:
        model = OrderListComment
        fields = ('content', 'order_list', 'commenter',)
        widgets = {'order_list': forms.HiddenInput(), 'commenter': forms.HiddenInput()}


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
