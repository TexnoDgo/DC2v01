# Generated by Django 3.1.4 on 2020-12-17 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CoatingPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('hex_color', models.CharField(max_length=10)),
                ('r_color', models.IntegerField()),
                ('g_color', models.IntegerField()),
                ('b_color', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('create', models.DateTimeField(default=django.utils.timezone.now)),
                ('c_type', models.CharField(choices=[('PART', 'PART'), ('ASSEMBLY', 'ASSEMBLY')], default='PART', max_length=20)),
                ('material', models.CharField(default='default', max_length=150)),
                ('thickness', models.CharField(default='0', max_length=10)),
                ('band_count', models.CharField(default='0', max_length=10)),
                ('draw_pdf', models.FileField(default='COMPONENT_DRAW_PDF/default.pdf', null=True, upload_to='COMPONENT_DRAW_PDF')),
                ('draw_png', models.FileField(default='COMPONENT_DRAW_PNG/default.png', null=True, upload_to='COMPONENT_DRAW_PNG')),
                ('dxf_file', models.FileField(default='COMPONENT_DXF_FILE/default.png', null=True, upload_to='COMPONENT_DXF_FILE')),
                ('part_file', models.FileField(default='COMPONENT_PART_FILE/default.png', null=True, upload_to='COMPONENT_PART_FILE')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CuttingPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MachiningPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('create', models.DateTimeField(default=django.utils.timezone.now)),
                ('readiness', models.DateField(null=True)),
                ('table', models.FileField(default=None, upload_to='ORDERS_TABLE')),
                ('qr_code_list', models.FileField(default=None, upload_to='ORDERS_QR_CODE_LIST')),
                ('pdf_specification', models.FileField(default=None, upload_to='ORDER_PDF_SPECIFICATION')),
                ('draw_archive', models.FileField(default=None, upload_to='ORDERS_DRAW_ARCHIVE')),
                ('dxf_archive', models.FileField(default=None, upload_to='ORDERS_DXF_ARCHIVE')),
                ('part_archive', models.FileField(default=None, upload_to='ORDERS_PART_ARCHIVE')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OtherPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('create', models.DateTimeField(default=django.utils.timezone.now)),
                ('active', models.BooleanField(default=False)),
                ('pdf_specification', models.FileField(default=None, upload_to='PROJECT_PDF_SPECIFICATION')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WorkApp.device')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('code', models.CharField(max_length=13)),
                ('qr_code', models.FileField(default=None, upload_to='POSITION_QR_CODE')),
                ('qr_code_production', models.FileField(default=None, upload_to='POSITION_QR_CODE_PRODUCTION')),
                ('sticker', models.FileField(default=None, upload_to='POSITION_STICKER')),
                ('sticker_draw_pdf', models.FileField(default=None, upload_to='POSITION_DRAW_PDF')),
                ('mather_assembly', models.CharField(default='default', max_length=255)),
                ('component', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='WorkApp.component')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WorkApp.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WorkApp.project'),
        ),
        migrations.CreateModel(
            name='OperationList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cutting', models.BooleanField(default=False)),
                ('machining', models.BooleanField(default=False)),
                ('coating', models.BooleanField(default=False)),
                ('other', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('CREATE', 'CREATE'), ('WORK', 'WORK'), ('DONE', 'DONE')], default='CREATE', max_length=250)),
                ('coating_place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WorkApp.coatingplace')),
                ('cutting_place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WorkApp.cuttingplace')),
                ('machining_place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WorkApp.machiningplace')),
                ('other_place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WorkApp.otherplace')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WorkApp.position')),
            ],
        ),
    ]
