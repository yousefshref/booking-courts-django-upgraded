# Generated by Django 3.2.25 on 2024-05-09 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='court',
            name='close_from',
        ),
        migrations.RemoveField(
            model_name='court',
            name='close_to',
        ),
        migrations.CreateModel(
            name='CourtCloseTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.court')),
            ],
        ),
    ]
