# Generated by Django 3.2.25 on 2024-04-30 16:30

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(db_index=True, max_length=100, unique=True)),
                ('email', models.EmailField(blank=True, db_index=True, max_length=254, null=True, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Academy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='academies/')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('location_url', models.CharField(blank=True, max_length=255, null=True)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AcademySubscribePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price_per_class', models.IntegerField(blank=True, default=0, null=True)),
                ('price_per_week', models.IntegerField(blank=True, default=0, null=True)),
                ('price_per_month', models.IntegerField(blank=True, default=0, null=True)),
                ('price_per_year', models.IntegerField(blank=True, default=0, null=True)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.academy')),
            ],
        ),
        migrations.CreateModel(
            name='AcademyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('phone', models.CharField(max_length=255, null=True)),
                ('date', models.DateField()),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('pinned_to', models.DateField(blank=True, null=True)),
                ('with_ball', models.BooleanField(default=False, null=True)),
                ('event_time', models.BooleanField(default=False, null=True)),
                ('offer_time', models.BooleanField(default=False, null=True)),
                ('is_paied', models.BooleanField(default=False, null=True)),
                ('paied_with', models.CharField(choices=[('عند الحضور', 'عند الحضور'), ('فودافون كاش', 'فودافون كاش')], max_length=255, null=True)),
                ('is_cancelled', models.BooleanField(default=False, null=True)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('location_url', models.CharField(blank=True, max_length=255, null=True)),
                ('price_per_hour', models.DecimalField(decimal_places=2, max_digits=10)),
                ('open_from', models.TimeField()),
                ('open_to', models.TimeField()),
                ('close_from', models.TimeField(blank=True, null=True)),
                ('close_to', models.TimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('ball_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('has_ball', models.BooleanField(default=True)),
                ('offer_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('offer_time_from', models.TimeField(blank=True, null=True)),
                ('offer_time_to', models.TimeField(blank=True, null=True)),
                ('event_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('event_time_from', models.TimeField(blank=True, null=True)),
                ('event_time_to', models.TimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.country')),
            ],
        ),
        migrations.CreateModel(
            name='CourtType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ManagerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='managers/')),
                ('brand_name', models.CharField(max_length=100, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('can_private_trainer', models.BooleanField(default=False)),
                ('can_academy', models.BooleanField(default=False)),
                ('can_courts', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WhiteList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='whitelist/')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='whitelist/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.managerprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VerificationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('uid', models.CharField(blank=True, max_length=100, null=True)),
                ('code', models.CharField(max_length=6)),
                ('is_used', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, default='', null=True, upload_to='users/')),
                ('bio', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='trainers/')),
                ('trainer', models.CharField(db_index=True, max_length=255, unique=True)),
                ('price_per_class', models.IntegerField(blank=True, default=0, null=True)),
                ('price_per_week', models.IntegerField(blank=True, default=0, null=True)),
                ('price_per_month', models.IntegerField(blank=True, default=0, null=True)),
                ('price_per_year', models.IntegerField(blank=True, default=0, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.managerprofile')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.academytype')),
            ],
        ),
        migrations.CreateModel(
            name='Subsribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_image', models.ImageField(blank=True, null=True, upload_to='subscribe/')),
                ('birth_cirtificate', models.ImageField(blank=True, null=True, upload_to='subscribe/')),
                ('national_id_image1', models.ImageField(blank=True, null=True, upload_to='subscribe/')),
                ('national_id_image2', models.ImageField(blank=True, null=True, upload_to='subscribe/')),
                ('national_id_parent1', models.ImageField(blank=True, null=True, upload_to='subscribe/')),
                ('national_id_parent2', models.ImageField(blank=True, null=True, upload_to='subscribe/')),
                ('passport_image', models.ImageField(blank=True, null=True, upload_to='subscribe/')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('birth_date', models.DateField(null=True)),
                ('gender', models.CharField(choices=[('ذكر', 'ذكر'), ('انثى', 'انثى')], max_length=255)),
                ('mother_phone', models.CharField(blank=True, max_length=255, null=True)),
                ('father_phone', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.IntegerField()),
                ('start_from', models.DateField(blank=True, null=True)),
                ('end_to', models.DateField(blank=True, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('academy_subscribe_plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.academysubscribeplan')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.managerprofile')),
                ('request_from_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.userprofile')),
                ('trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.city')),
            ],
        ),
        migrations.CreateModel(
            name='StaffProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.managerprofile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_warning', models.CharField(blank=True, max_length=100, null=True)),
                ('limit_of_paying_in_minuts', models.IntegerField(blank=True, default=0, null=True)),
                ('limit_of_canceling_in_minuts', models.IntegerField(blank=True, default=0, null=True)),
                ('manager', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.managerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='PinnedTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('is_cancelled', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.book')),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('created_time', models.TimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.managerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('created_time', models.TimeField(auto_now_add=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.managerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='CourtVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.court')),
            ],
        ),
        migrations.CreateModel(
            name='CourtTool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.court')),
            ],
        ),
        migrations.CreateModel(
            name='CourtImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/courts/')),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.court')),
            ],
        ),
        migrations.CreateModel(
            name='CourtFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('is_free', models.BooleanField(blank=True, default=False, null=True)),
                ('court', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.court')),
            ],
        ),
        migrations.AddField(
            model_name='court',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.managerprofile'),
        ),
        migrations.AddField(
            model_name='court',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.state'),
        ),
        migrations.AddField(
            model_name='court',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.courttype'),
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.country'),
        ),
        migrations.AddField(
            model_name='book',
            name='court',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.court'),
        ),
        migrations.AddField(
            model_name='book',
            name='tools',
            field=models.ManyToManyField(blank=True, null=True, to='api.CourtTool'),
        ),
        migrations.AddField(
            model_name='book',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='AcademyTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_name', models.CharField(max_length=255)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('academy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.academy')),
            ],
        ),
        migrations.AddField(
            model_name='academy',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.managerprofile'),
        ),
        migrations.AddField(
            model_name='academy',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.academytype'),
        ),
    ]
