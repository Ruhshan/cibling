from django import forms
from django.forms import fields
from .models import Post, Comment

class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['content', 'image']


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'rows':2,
        })
    )

    class Meta:
        model = Comment
        fields = ['text']