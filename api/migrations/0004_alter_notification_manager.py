# Generated by Django 3.2.25 on 2024-05-09 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20240509_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='api.managerprofile'),
        ),
    ]
