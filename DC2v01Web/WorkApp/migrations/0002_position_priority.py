# Generated by Django 3.1.4 on 2020-12-21 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]
