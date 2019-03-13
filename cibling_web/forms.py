from django import forms
from django.forms import fields
from .models import Post, Comment
from users.models import Country, Institute, Subject, Expertise

class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    content = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(
            attrs={'rows':5,}
        )
    )

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

class CountryForm(forms.ModelForm):
    choose_country = forms.ModelChoiceField(queryset=Country.objects)

    class Meta:
        model = Country
        fields = ['choose_country']

class InstituteForm(forms.ModelForm):
    choose_institute = forms.ModelChoiceField(queryset=Institute.objects)

    class Meta:
        model = Institute
        fields =['choose_institute']

class SubjectForm(forms.ModelForm):
    choose_subject = forms.ModelChoiceField(queryset=Subject.objects)

    class Meta:
        model = Subject
        fields =['choose_subject']

class ExpertiseForm(forms.ModelForm):
    choose_expertise = forms.ModelChoiceField(queryset=Expertise.objects)

    class Meta:
        model = Expertise
        fields =['choose_expertise']