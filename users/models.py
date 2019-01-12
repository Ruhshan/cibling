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
    institute = models.ForeignKey(Institute, on_delete=Institute.objects.filter(institute='unknown').first(), null= True, default=Institute.objects.filter(institute='unknown').first())
    country = models.ForeignKey(Country, on_delete=Country.objects.filter(country='unknown').first(), null=True, default=Country.objects.filter(country='unknown').first())
    date_of_birth = models.DateField(default='2001-01-01',null = True)



    def __str__(self):
        return '{} Profile'.format(self.user.username)