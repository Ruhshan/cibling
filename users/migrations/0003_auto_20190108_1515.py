# Generated by Django 2.1.4 on 2019-01-08 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190108_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cover_image',
            field=models.ImageField(default='default.jpg', null=True, upload_to='cover_pics/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics/'),
        ),
    ]
