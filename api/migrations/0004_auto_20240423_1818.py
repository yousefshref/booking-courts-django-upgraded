# Generated by Django 3.2.25 on 2024-04-23 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20240423_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='name',
            field=models.CharField(default='لا يوجد اسم', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='paied_with',
            field=models.CharField(choices=[('عند الحضور', 'عند الحضور'), ('فودافون كاش', 'فودافون كاش')], default='عند الحضور', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='phone',
            field=models.CharField(default='01010101010', max_length=255, null=True),
        ),
    ]
