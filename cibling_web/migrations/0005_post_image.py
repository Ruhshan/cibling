# Generated by Django 2.1.4 on 2019-01-08 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cibling_web', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default.jpg', null=True, upload_to='post_pics/'),
        ),
    ]
