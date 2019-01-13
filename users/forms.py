from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Profile, Institute, Country


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    date_of_birth = forms.DateField()
    institute = forms.ModelChoiceField(queryset=Institute.objects)

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'date_of_birth', 'institute', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        institute = self.cleaned_data.get('institute')
        date_of_birth = self.cleaned_data.get('date_of_birth')
        country = institute.country
        if commit:
            user.save()
        Profile.objects.create(user=user,institute=institute,date_of_birth=date_of_birth, country=country)
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'date_of_birth', 'password1', 'password2']