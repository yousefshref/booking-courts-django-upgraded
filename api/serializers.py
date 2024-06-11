from rest_framework import serializers
from . import models
from.models import CourtImage, CourtVideo, CourtFeature, CourtTool




class NotificationSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Notification
    fields = '__all__'

class ManagerProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.ManagerProfile
    fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.UserProfile
    fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
  manager_details = ManagerProfileSerializer(source='manager', required=False)
  user_details = UserProfileSerializer(source='user', required=False)
  class Meta(object):
    model = models.CustomUser
    fields = '__all__'


class ManagerProfileSerializer(serializers.ModelSerializer):
  user_details = UserSerializer(source='user', read_only=True)
  class Meta:
    model = models.ManagerProfile
    fields = '__all__'

class StaffProfileSerializer(serializers.ModelSerializer):
  user_details = UserSerializer(source='user', read_only=True)
  class Meta:
    model = models.StaffProfile
    fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
  user_details = UserSerializer(source='user', read_only=True)
  class Meta:
    model = models.UserProfile
    fields = '__all__'




class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = '__all__'


class CourtCloseTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourtCloseTime
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = '__all__'


class CourtTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourtType
        fields = '__all__'




class CourtImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtImage
        fields = '__all__'



class CourtVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtVideo
        fields = '__all__'

class CourtFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtFeature
        fields = '__all__'

class CourtToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtTool
        fields = '__all__'

class CourtSerializer(serializers.ModelSerializer):
  country_details = CountrySerializer(source='country', read_only=True)
  city_details = CitySerializer(source='city', read_only=True)
  state_details = StateSerializer(source='state', read_only=True)
  profile_details = ManagerProfileSerializer(source='manager', read_only=True)
  close_times_details = CourtCloseTimeSerializer(source='close_times', read_only=True, many=True)
  images_details = CourtImageSerializer(source='images', read_only=True, many=True)
  video_details = CourtVideoSerializer(source='videos', read_only=True, many=True)
  features_details = CourtFeatureSerializer(source='features', read_only=True, many=True)
  tools_details = CourtToolSerializer(source='tools', read_only=True, many=True)
  class Meta:
    model = models.Court
    fields = '__all__'



class BookSerializer(serializers.ModelSerializer):
  court_details = CourtSerializer(source='court', read_only=True)
  class Meta:
    model = models.Book
    fields = '__all__'

class PinnedTimeSerializer(serializers.ModelSerializer):
  book_details = BookSerializer(source='book', read_only=True)
  class Meta:
    model = models.PinnedTime
    fields = '__all__'


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Setting
        fields = '__all__'


class WhiteListSerializer(serializers.ModelSerializer):
  user_detail = UserSerializer(source='user', read_only=True)
  class Meta:
      model = models.WhiteList
      fields = '__all__'











class AcademyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AcademyType
        fields = '__all__'


class AcademySerializer(serializers.ModelSerializer):
  type_details = AcademyTypeSerializer(source='type', read_only=True)
  manager_details = ManagerProfileSerializer(source='manager', read_only=True)
  class Meta:
    model = models.Academy
    fields = '__all__'



class AcademyTimeSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.AcademyTime
    fields = '__all__'


class TrainerSerializer(serializers.ModelSerializer):
  manager_details = ManagerProfileSerializer(source='manager', read_only=True)
  type_details = AcademyTypeSerializer(source='type', read_only=True)
  class Meta:
    model = models.Trainer
    fields = '__all__'


class AcademySubscribePlanSerializer(serializers.ModelSerializer):
  academy_details = AcademySerializer(source='academy', read_only=True)
  trainer_details = TrainerSerializer(source='plans_trainer', read_only=True)
  class Meta:
    model = models.AcademySubscribePlan
    fields = '__all__'






class IncomeSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Income
    fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Expense
    fields = '__all__'




class SubsribeSerializer(serializers.ModelSerializer):
  manager_details = ManagerProfileSerializer(source='manager', read_only=True)
  trainer_details = TrainerSerializer(source='trainer', read_only=True)
  academy_subscribe_plan_details = AcademySubscribePlanSerializer(source='academy_subscribe_plan', read_only=True)
  class Meta:
    model = models.Subsribe
    fields = '__all__'






