"""Формы"""

from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Форма для комментария
    """

    class Meta:
        model = Comment
        fields = ('content',)
