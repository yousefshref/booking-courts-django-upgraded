# Generated by Django 3.2.25 on 2024-04-23 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20240423_1920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='name_ar',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='name',
            field=models.CharField(default='لا يوجد اسم', max_length=255, null=True, verbose_name='الاسم'),
        ),
    ]