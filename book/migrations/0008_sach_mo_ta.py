# Generated by Django 4.0.3 on 2022-05-25 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_alter_sach_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='sach',
            name='mo_ta',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
