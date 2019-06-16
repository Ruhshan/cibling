from django.db import models
from django.contrib.auth.models import User


class CustomUser(User):
    institute = models.TextField()
    country = models.TextField()
    date_of_birth = models.DateField()


class Country(models.Model):
    country = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.country

class Subject(models.Model):
    subject = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.subject

class Expertise(models.Model):
    expertise = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.expertise

class Interest(models.Model):
    interest = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.interest

class Language(models.Model):
    language = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.language



class Institute(models.Model):
    institute = models.CharField(unique=True, max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return '{institute}, {country}'.format(institute=self.institute, country = self.country.country)


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics/')
    cover_image = models.ImageField(default='default.jpg', upload_to='cover_pics/', null=True)
    institute = models.ForeignKey(Institute, on_delete=None, null= True, default=None)
    #country = models.ForeignKey(Country, on_delete=None, null=True, default=None)
    date_of_birth = models.DateField(default='2001-01-01',null = True)



    def __str__(self):
        return '{} Profile'.format(self.user.username)


class ProfileInfo(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    expertises = models.ManyToManyField(Expertise, related_name='profiles', null=True)
    interests = models.ManyToManyField(Interest, related_name='profiles', null=True)
    languages = models.ManyToManyField(Language, related_name='profiles', null=True)
    personal_info = models.CharField(null=True, max_length=1000)
    subject = models.ForeignKey(Subject, on_delete=None, null=True)

    def __str__(self):
        return '{} Profile Info'.format(self.profile.user.username)



class Cibling(models.Model):
    cibling_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cibling_1')
    cibling_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cibling_2')
    status = models.BooleanField(default=False)

    def __str__(self):
        return 'Cibling between {c1} and {c2}'.format(c1=self.cibling_1.first_name+' '+self.cibling_1.last_name,c2=self.cibling_2.first_name+' '+self.cibling_2.last_name)
