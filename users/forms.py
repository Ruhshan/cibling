from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Profile, Institute, ProfileInfo, Country, Subject, Expertise, Interest
from .listtextwidget import ListTextWidget, ListTextWidgetDynamic, TagWidget
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

    institute = forms.CharField(widget=ListTextWidgetDynamic("institute", name='institute-list',attrs={"v-on:focus":"focused"}))
    country = forms.ModelChoiceField(queryset=Country.objects, widget=forms.Select(attrs={'v-model':"country"}))
    subject = forms.CharField(widget=ListTextWidget(Subject.objects.all().values_list('subject', flat=True), name='subject-list', attrs={'v-model':"subject"}))
    expertise = forms.CharField(widget=TagWidget(name="expertise",selectedTagsModel="selectedExpertises",existingTagsModel="existingExpertises"))
    interest = forms.CharField(widget=TagWidget(name="interest",selectedTagsModel="selectedInterests",existingTagsModel="existingInterests"))

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2', 'date_of_birth', 'country',
                  'institute','subject', 'expertise', 'interest']

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

    def clean_institute(self):
        data = self.cleaned_data["institute"]
        if len(data) < 5:
            raise forms.ValidationError("Provide full name of your institution")
        return data

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        
        date_of_birth = self.cleaned_data.get('date_of_birth')
        country = self.cleaned_data.get('country')
        institute = Institute.objects.get_or_create(institute=self.cleaned_data.get('institute').title(), country=Country.objects.get(country=country))
        subject = Subject.objects.get_or_create(subject=self.cleaned_data.get('subject').title())
        expertise = self.cleaned_data["expertise"]
        interest = self.cleaned_data["interest"]

        #if commit:
            #user.save()
        #profile = Profile.objects.create(user=user,institute=institute,date_of_birth=date_of_birth)
        expertises = []
        interests = []
        for e in expertise.split(","):
            try:
                exp = Expertise.objects.get(id=e) if e.isdigit() else Expertise.objects.get_or_create(expertise=e.title())
                expertises.append(exp)
            except Exception as excptn:
                print(excptn)
            print(expertises)

        for i in interest.split(","):
            try:
                intrst = Interest.objects.get(id=i) if i.isdigit() else Interest.objects.get_or_create(interest=i.title())
                interests.append(intrst)
            except Exception as excptn:
                print(excptn)

            print(interests)

        # profile_info = ProfileInfo.objects.create(profile=profile, subject=subject)
        # profile_info.expertises.add(expertises)
        # profile_info.interests.add(interests)
        # profile_info.save()

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