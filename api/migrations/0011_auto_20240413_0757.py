# Generated by Django 3.2.25 on 2024-04-13 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20240413_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='limit_of_canceling_in_minuts',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='setting',
            name='limit_of_paying_in_minuts',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
