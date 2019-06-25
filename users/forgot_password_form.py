from django import forms
from django.contrib.auth.models import User


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Please enter your email'}))

    def clean_email(self):
        data = self.cleaned_data["email"]
        if not User.objects.filter(email=data).exists():
            raise forms.ValidationError("No account with this email found!")
        return data

