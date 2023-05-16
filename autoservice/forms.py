from .models import OrderListComment
from django import forms


class OrderListCommentForm(forms.ModelForm):
    class Meta:
        model = OrderListComment
        fields = ('content', 'order_list', 'commenter',)
        widgets = {'order_list': forms.HiddenInput(), 'commenter': forms.HiddenInput()}
