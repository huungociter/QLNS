# Generated by Django 3.1.8 on 2022-06-08 18:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0016_auto_20220609_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sach',
            name='ngay_nhap',
            field=models.DateField(default=django.utils.timezone.now, null=True),
        ),
    ]
