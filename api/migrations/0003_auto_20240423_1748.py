# Generated by Django 3.2.25 on 2024-04-23 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20240422_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='father_phone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], default='male', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='mother_phone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='nationality',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='paied_with',
            field=models.CharField(blank=True, choices=[('عند الحضور', 'عند الحضور'), ('فودافون كاش', 'فودافون كاش')], default='عند الحضور', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='academy',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='academies/'),
        ),
        migrations.AlterField(
            model_name='courtimage',
            name='image',
            field=models.ImageField(upload_to='images/courts/'),
        ),
        migrations.AlterField(
            model_name='whitelist',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='whitelist/'),
        ),
        migrations.AlterField(
            model_name='whitelist',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='whitelist/'),
        ),
        migrations.CreateModel(
            name='Championship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('champion_name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='championship/')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='championship/')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='championship/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.invoice')),
            ],
        ),
    ]