# Generated by Django 3.1.4 on 2021-01-08 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkApp', '0004_auto_20210105_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationlist',
            name='notes',
            field=models.CharField(default='None', max_length=255),
        ),
    ]