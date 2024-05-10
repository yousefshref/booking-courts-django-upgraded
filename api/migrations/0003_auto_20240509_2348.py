# Generated by Django 3.2.25 on 2024-05-09 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20240509_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academysubscribeplan',
            name='academy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plans', to='api.academy'),
        ),
        migrations.AlterField(
            model_name='academytime',
            name='academy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='times', to='api.academy'),
        ),
        migrations.AlterField(
            model_name='courtclosetime',
            name='court',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='close_times', to='api.court'),
        ),
        migrations.AlterField(
            model_name='courtfeature',
            name='court',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='features', to='api.court'),
        ),
        migrations.AlterField(
            model_name='courtimage',
            name='court',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='api.court'),
        ),
        migrations.AlterField(
            model_name='courttool',
            name='court',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tools', to='api.court'),
        ),
        migrations.AlterField(
            model_name='courtvideo',
            name='court',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='api.court'),
        ),
        migrations.AlterField(
            model_name='managerprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='manager', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='api.userprofile')),
            ],
        ),
    ]