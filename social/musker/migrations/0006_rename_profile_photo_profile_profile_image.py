# Generated by Django 5.0.3 on 2024-03-22 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musker', '0005_profile_profile_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='profile_photo',
            new_name='profile_image',
        ),
    ]