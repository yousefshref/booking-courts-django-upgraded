# Generated by Django 3.2.25 on 2024-04-19 21:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_auto_20240419_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 19, 23, 29, 49, 370670)),
        ),
    ]
