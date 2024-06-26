from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction

from .models import CustomUser, Profile, Institute, ProfileInfo, Country, Subject, Expertise, Interest, Offer, Language
from .listtextwidget import ListTextWidget, ListTextWidgetDynamic, TagWidget
# for writing validator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import json

def validate_ac(value):
    print(value)
    if '.ac.' not in value:
        raise ValidationError(_("Please enter your academic email"))
    else:
        return value


class UserRegisterForm(UserCreationForm):
    # email = forms.EmailField(help_text='Please enter your academic email', validators=[validate_ac])
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Please enter your email'}))
    years = [i for i in range(1940, 2001)]
    date_of_birth = forms.DateField(initial='YYYY-MM-DD')

    institute = forms.CharField(
        widget=ListTextWidgetDynamic("institute", name='institute-list', attrs={"v-on:focus": "focused","placeholder":
            "Enter official name of your institution"}))
    country = forms.ModelChoiceField(queryset=Country.objects, widget=forms.Select(attrs={"ref":"country"}))
    subject = forms.CharField(
        widget=ListTextWidget(Subject.objects.all().values_list('subject', flat=True), name='subject-list',
                              attrs={"placeholder":"Enter the subject of your study"}))
    expertise = forms.CharField(widget=TagWidget(name="expertise", selectedTagsModel="selectedExpertises",
                                                 existingTagsModel="existingExpertises"))
    interest = forms.CharField(
        widget=TagWidget(name="interest", selectedTagsModel="selectedInterests", existingTagsModel="existingInterests"))


    offer = forms.ModelMultipleChoiceField(queryset=Offer.objects.all(), required=False)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'date_of_birth', 'country',
                  'institute', 'subject', 'expertise', 'interest', 'offer']
        widgets = {
            'username': forms.fields.TextInput(attrs={'placeholder': '150 characters or fewer. Letters, digits and @/./+/-/_ only.'}),
        }


    def clean_institute(self):
        data = self.cleaned_data["institute"]
        if len(data) < 5:
            raise forms.ValidationError("Provide full name of your institution")
        return data

    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("User with this email already exists")
        return data

    def clean_expertise(self):
        data = self.cleaned_data["expertise"]
        return data


    @transaction.atomic
    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)

        date_of_birth = self.cleaned_data.get('date_of_birth')
        country = self.cleaned_data.get('country')
        institute, _ = Institute.objects.get_or_create(institute=self.cleaned_data.get('institute').title(),
                                                       country=Country.objects.get(country=country))
        subject, _ = Subject.objects.get_or_create(subject=self.cleaned_data.get('subject').title())
        expertise = json.loads(self.cleaned_data["expertise"])
        interest = json.loads(self.cleaned_data["interest"])

        offer = self.cleaned_data["offer"]

        if commit:
            user.is_active = False
            user.is_staff = False
            user.save()

        profile = Profile.objects.create(user=user,
                                         institute=institute,
                                         date_of_birth=date_of_birth)

        profile_info = ProfileInfo.objects.get(profile=profile)

        for e in expertise:
            try:
                exp, _ = (Expertise.objects.get(id=e['key']), _) if e['key'].isdigit() else Expertise.objects.get_or_create(
                    expertise=e['value'].title())
                profile_info.expertises.add(exp)
            except Exception as excptn:
                print(excptn)

        for i in interest:
            try:
                intrst, _ = (Interest.objects.get(id=i['key']), _) if i['key'].isdigit() else Interest.objects.get_or_create(
                    interest=i['value'].title())
                profile_info.interests.add(intrst)
            except Exception as excptn:
                print(excptn)

        for o in offer:
            try:
                profile_info.offers.add(o)
            except Exception as excptn:
                print(excptn)

        profile_info.save()

        return user

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Enter a strong password containing at least 8 mixed character'
        self.fields['username'].help_text = ""
        self.fields['offer'].widget.attrs = {"class":"selectpicker"}


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        data = self.cleaned_data["email"]
        if not User.objects.filter(email=data).exists():
            raise forms.ValidationError("No user found with this email!")
        return data

    def clean_password(self):
        data = self.cleaned_data["password"]
        if "email" in self.cleaned_data.keys():
            user = User.objects.filter(email=self.cleaned_data["email"])

            if user and not user.first().check_password(data):
                raise forms.ValidationError("Username and Password doesn't match")
            return data


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

class InstituteUpdateForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects, widget=forms.Select(attrs={"ref": "country"}))
    institute = forms.CharField(
        widget=ListTextWidgetDynamic("institute", name='institute-list', attrs={"v-on:focus": "focused", "placeholder":
            "Enter official name of your institution"}))

    def clean_institute(self):
        data = self.cleaned_data["institute"]
        institute, _ = Institute.objects.get_or_create(institute=data.title(),
                                                       country=Country.objects.get(country=self.cleaned_data["country"]))
        return institute

    class Meta:
        model = Profile
        fields = ['country','institute']


class ProfileInfoUpdateForm(forms.ModelForm):
    subject = forms.CharField(
        widget=ListTextWidget(Subject.objects.all(), name='subject-list',
                              attrs={"placeholder": "Enter the subject of your study"}))
    expertises = forms.CharField(widget=TagWidget(name="expertises", selectedTagsModel="selectedExpertises",
                                                 existingTagsModel="existingExpertises"))
    interests = forms.CharField(
        widget=TagWidget(name="interests", selectedTagsModel="selectedInterests", existingTagsModel="existingInterests"))
    languages = forms.CharField(
        widget=TagWidget(name="languages", selectedTagsModel="selectedLanguages", existingTagsModel="existingLanguages"))

    class Meta:
        model = ProfileInfo
        fields = ['personal_info', 'subject','offers', 'languages','expertises', 'interests']

    def clean_subject(self):
        data = self.cleaned_data["subject"]
        subject, _ = Subject.objects.get_or_create(subject=data.title())
        return subject

    def clean_expertises(self):
        expertises = []
        data = self.cleaned_data["expertises"]
        for e in json.loads(data):
            try:
                exp, _ = (Expertise.objects.get(id=e["key"]), _) if e["key"].isdigit() else Expertise.objects.get_or_create(
                    expertise=e["value"].title())

                expertises.append(exp)
            except Exception as excptn:
                print(excptn)

        return expertises

    def clean_interests(self):
        interests = []
        data = self.cleaned_data["interests"]
        for i in json.loads(data):
            try:
                intrst, _ = (Interest.objects.get(id=i["key"]), _) if i["key"].isdigit() else Interest.objects.get_or_create(
                    interest=i["value"].title())
                interests.append(intrst)
            except Exception as excptn:
                print(excptn)
        return interests

    def clean_languages(self):
        languages = []
        data = self.cleaned_data["languages"]
        for l in json.loads(data):
            try:
                lngz, _ = (Language.objects.get(id=l["key"]),_) if l["key"].isdigit() else Language.objects.get_or_create(
                    language = l["value"].title())
                languages.append(lngz)
            except Exception as excptn:
                print(excptn)
        return languages



    def __init__(self, *args, **kwargs):
        super(ProfileInfoUpdateForm, self).__init__(*args, **kwargs)
        self.fields['offers'].widget.attrs = {"class": "selectpicker"}



