# Generated by Django 3.1.4 on 2021-01-11 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0003_profile_new_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_user_last',
            field=models.CharField(default='Фамилия', max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_user_name',
            field=models.CharField(default='Имя', max_length=20),
        ),
    ]