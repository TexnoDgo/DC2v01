# Generated by Django 3.1.4 on 2021-01-05 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkApp', '0003_position_storage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operationlist',
            name='status',
        ),
        migrations.AddField(
            model_name='operationlist',
            name='coating_status',
            field=models.CharField(choices=[('NONE', 'NONE'), ('CREATE', 'CREATE'), ('WORK', 'WORK'), ('DONE', 'DONE')], default='NONE', max_length=20),
        ),
        migrations.AddField(
            model_name='operationlist',
            name='cutting_status',
            field=models.CharField(choices=[('NONE', 'NONE'), ('CREATE', 'CREATE'), ('WORK', 'WORK'), ('DONE', 'DONE')], default='NONE', max_length=20),
        ),
        migrations.AddField(
            model_name='operationlist',
            name='general_status',
            field=models.CharField(choices=[('NONE', 'NONE'), ('CREATE', 'CREATE'), ('WORK', 'WORK'), ('DONE', 'DONE')], default='CREATE', max_length=20),
        ),
        migrations.AddField(
            model_name='operationlist',
            name='machining_status',
            field=models.CharField(choices=[('NONE', 'NONE'), ('CREATE', 'CREATE'), ('WORK', 'WORK'), ('DONE', 'DONE')], default='NONE', max_length=20),
        ),
        migrations.AddField(
            model_name='operationlist',
            name='other_status',
            field=models.CharField(choices=[('NONE', 'NONE'), ('CREATE', 'CREATE'), ('WORK', 'WORK'), ('DONE', 'DONE')], default='NONE', max_length=20),
        ),
    ]
