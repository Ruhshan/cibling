from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Profile, Institute, ProfileInfo

#for writing validator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_ac(value):
    print(value)
    if '.ac.' not in value:
        raise ValidationError(_("Please enter your academic email"))
    else:
        return value

class UserRegisterForm(UserCreationForm):
    #email = forms.EmailField(help_text='Please enter your academic email', validators=[validate_ac])
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Please enter your first part of the name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Please enter your last part of the name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Please enter your email'}),
                             help_text='Email should be your academic email')
    years = [i for i in range(1940,2001)]
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'Select your date of birth'}),
                                    help_text='Format: YYYY-MM-DD')
    institute = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Please enter the name of your institution'}))

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'date_of_birth', 'institute', 'password1', 'password2']
    '''
    def is_valid(self):
        valid = super(UserRegisterForm, self).is_valid()

        if valid:
            email = self.cleaned_data.get('email')
            if email.find('.aac.') != -1:
                return True
        else:
            return False
    '''

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        institute = self.cleaned_data.get('institute')
        date_of_birth = self.cleaned_data.get('date_of_birth')
        country = institute.country
        if commit:
            user.save()
        Profile.objects.create(user=user,institute=institute,date_of_birth=date_of_birth)
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'date_of_birth', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'cover_image', 'institute', 'date_of_birth']

class ProfileInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = ProfileInfo
        fields = ['personal_info', 'subject', 'expertises', 'interests', 'languages']