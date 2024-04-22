from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver



class CustomUser(AbstractUser):
  phone = models.CharField(max_length=100, unique=True, db_index=True)
  email = models.EmailField(max_length=254, unique=True, db_index=True, null=True, blank=True)
  def __str__(self):
    return self.username

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)


class VerificationCode(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
  email = models.EmailField(null=True, blank=True)
  phone = models.CharField(max_length=100, null=True, blank=True)
  uid = models.CharField(max_length=100, null=True, blank=True)
  code = models.CharField(max_length=6)
  is_used = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

class ManagerProfile(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  is_verified = models.BooleanField(default=False)

  can_academy = models.BooleanField(default=False)
  can_courts = models.BooleanField(default=False)

  def __str__(self):
    return self.user.username
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)


class StaffProfile(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  manager = models.ForeignKey(ManagerProfile, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.username

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)


class Setting(models.Model):
  manager = models.OneToOneField(ManagerProfile, on_delete=models.CASCADE)
  # courts settings
  booking_warning = models.CharField(null=True, blank=True, max_length=100)
  limit_of_paying_in_minuts = models.IntegerField(default=0, null=True, blank=True) # if null or 0 can pay any time
  limit_of_canceling_in_minuts = models.IntegerField(default=0, null=True, blank=True) # if null or 0 can cancell any time

  def __str__(self):
    return self.manager.user.username


class UserProfile(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.user.username

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)



class Country(models.Model):
  name = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

class City(models.Model):
  country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
  name = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

class State(models.Model):
  city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
  name = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)



class Court(models.Model):
  manager = models.ForeignKey(ManagerProfile, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  address = models.CharField(max_length=255)
  location_url = models.CharField(max_length=255, null=True, blank=True)

  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  city = models.ForeignKey(City, on_delete=models.CASCADE)
  state = models.ForeignKey(State, on_delete=models.CASCADE)

  price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

  open_from = models.TimeField()
  open_to = models.TimeField()
  close_from = models.TimeField(null=True, blank=True)
  close_to = models.TimeField(null=True, blank=True)

  is_active = models.BooleanField(default=False)
  
  ball_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
  has_ball = models.BooleanField(default=True)

  offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
  offer_time_from = models.TimeField(null=True, blank=True)
  offer_time_to = models.TimeField(null=True, blank=True)
  

  event_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
  event_time_from = models.TimeField(null=True, blank=True)
  event_time_to = models.TimeField(null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    if self.manager.is_verified:
      self.is_active = True
    super().save()


class CourtImage(models.Model):
  court = models.ForeignKey(Court, on_delete=models.CASCADE)
  image = models.ImageField(upload_to='images/courts/')

  def __str__(self):
    return self.image.url
  
  
class CourtVideo(models.Model):
  court = models.ForeignKey(Court, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  url = models.URLField()

  def __str__(self):
    return self.name


class CourtFeature(models.Model):
  court = models.ForeignKey(Court, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=255, null=True, blank=True)
  is_free = models.BooleanField(default=False, null=True, blank=True)

  def __str__(self):
    return self.name


class CourtTool(models.Model):
  court = models.ForeignKey(Court, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  
  def __str__(self):
    return self.name
  


paied_with_choices = (
  ('عند الحضور', 'عند الحضور'),
  ('فودافون كاش', 'فودافون كاش'),
)

from datetime import datetime, timedelta
class Book(models.Model):
  court = models.ForeignKey(Court, on_delete=models.CASCADE)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  
  name = models.CharField(max_length=255, null=True)
  phone = models.CharField(max_length=255, null=True)
  date = models.DateField()
  
  start_time = models.TimeField(null=True)
  end_time = models.TimeField(null=True)
  

  pinned_to = models.DateField(null=True, blank=True)

  with_ball = models.BooleanField(default=False, null=True)
  event_time = models.BooleanField(default=False, null=True)
  offer_time = models.BooleanField(default=False, null=True)

  is_paied = models.BooleanField(default=False, null=True)
  paied_with = models.CharField(choices=paied_with_choices, max_length=255, null=True)

  is_cancelled = models.BooleanField(default=False, null=True)

  total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0, blank=True)

  tools = models.ManyToManyField(CourtTool, blank=True, null=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.court.name

  @classmethod
  def between_dates(cls, start, end):
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')

    # Initialize the list to store dates
    dates_between = []

    # Start with the first date
    current_date = start_date

    # Loop until the current date is less than or equal to the end date
    while current_date <= end_date:
      # Add the current date to the list
      dates_between.append(current_date.strftime('%Y-%m-%d'))
      # Increment the current date by 7 days
      current_date += timedelta(days=7)
    
    return dates_between


  def save(self, *args, **kwargs):
    if self.pinned_to:
        PinnedTime.objects.filter(book=self).delete()
        dates_between = self.between_dates(str(self.date), str(self.pinned_to))

        for d in dates_between:
            if not PinnedTime.objects.filter(book=self, date=d).exists():
                PinnedTime.objects.create(book=self, date=d)
            else:
                pass
    elif self.pinned_to is None or not self.pinned_to:
      PinnedTime.objects.filter(book=self).delete()

    super().save(*args, **kwargs)

    
    total_price = 0

    if self.offer_time and self.court.offer_time:
      total_price += self.court.offer_time

    elif self.event_time and self.court.event_time_from and self.court.event_time_to:
      total_price += self.court.event_price

    else:
      total_price += self.court.price_per_hour

    if self.with_ball and self.court.ball_price:
      total_price += self.court.ball_price

    tools = []
    if len(tools) > 0:
      tools = self.tools.all()
      for t in tools:
        total_price += t.price


    self.total_price = total_price

    super().save()



class PinnedTime(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
  date = models.DateField()
  is_cancelled = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.book.court.name)+" - "+ str(self.date)

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)




class AcademyType(models.Model):
  name = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name



class Academy(models.Model):
  manager = models.ForeignKey(ManagerProfile, on_delete=models.CASCADE)
  image = models.ImageField(upload_to='academies/', null=True, blank=True)
  name = models.CharField(max_length=255)
  type = models.ForeignKey(AcademyType, on_delete=models.CASCADE)
  location = models.CharField(max_length=255)
  location_url = models.CharField(max_length=255, null=True, blank=True)
  website = models.CharField(max_length=255, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name


class AcademyTime(models.Model):
  academy = models.ForeignKey(Academy, on_delete=models.CASCADE)
  day_name = models.CharField(max_length=255)
  start_time = models.TimeField(null=True, blank=True)
  end_time = models.TimeField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(self.academy.name)



class AcademySubscribePlan(models.Model):
  academy = models.ForeignKey(Academy, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  price_per_class = models.IntegerField(null=True, blank=True, default=0)
  price_per_week = models.IntegerField(null=True, blank=True, default=0)
  price_per_month = models.IntegerField(null=True, blank=True, default=0)
  price_per_year = models.IntegerField(null=True, blank=True, default=0)
  description = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.academy.name)+" - "+ str(self.name)



class AcademyTrainer(models.Model):
  manager = models.ForeignKey(ManagerProfile, on_delete=models.CASCADE, null=True)
  trainer = models.CharField(max_length=255, unique=True, db_index=True)
  type = models.ForeignKey(AcademyType, on_delete=models.CASCADE)
  price_per_class = models.IntegerField(null=True, blank=True, default=0)
  price_per_week = models.IntegerField(null=True, blank=True, default=0)
  price_per_month = models.IntegerField(null=True, blank=True, default=0)
  price_per_year = models.IntegerField(null=True, blank=True, default=0)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(self.type.name)+" - "+ str(self.trainer)





class Invoice(models.Model):
  manager = models.ForeignKey(ManagerProfile, on_delete=models.CASCADE, null=True)
  
  court = models.ForeignKey('Court', on_delete=models.CASCADE, null=True, blank=True)
  book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True, blank=True)
  academy = models.ForeignKey(Academy, on_delete=models.CASCADE, null=True, blank=True)

  name = models.CharField(max_length=255, null=True, blank=True)
  phone = models.CharField(max_length=255, null=True, blank=True)

  start_date = models.DateField(null=True, blank=True)
  end_date = models.DateField(null=True, blank=True)

  amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)

  description = models.TextField(null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.manager.user.username

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)






class WhiteList(models.Model):
  manager = models.ForeignKey(ManagerProfile, on_delete=models.CASCADE)

  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  phone = models.CharField(max_length=255)
  image = models.ImageField(upload_to='whitelist/', null=True, blank=True)
  image2 = models.ImageField(upload_to='whitelist/', null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user.username






