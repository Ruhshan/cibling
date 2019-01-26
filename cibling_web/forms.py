from django import forms
from django.forms import fields
from .models import Post

class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['content', 'image']
