# Generated by Django 3.1.4 on 2021-01-11 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(default='+38(099) 099-99-99', max_length=20),
        ),
    ]
