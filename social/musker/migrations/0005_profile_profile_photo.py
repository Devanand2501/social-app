# Generated by Django 5.0.3 on 2024-03-09 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musker', '0004_tweet'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
