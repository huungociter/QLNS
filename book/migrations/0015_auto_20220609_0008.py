# Generated by Django 3.1.8 on 2022-06-08 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0014_alter_hoadon_da_tra_alter_hoadon_tong_tien'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chitiethoadon',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='debt',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sach',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]