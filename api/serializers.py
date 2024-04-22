from rest_framework import serializers
from . import models
from.models import CourtImage, CourtVideo, CourtFeature, CourtTool

class UserSerializer(serializers.ModelSerializer):
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

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Invoice
        fields = '__all__'



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = '__all__'


class CourtSerializer(serializers.ModelSerializer):
  country_details = CountrySerializer(source='country', read_only=True)
  city_details = CitySerializer(source='city', read_only=True)
  state_details = StateSerializer(source='state', read_only=True)
  class Meta:
    model = models.Court
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


class AcademyTrainerSerializer(serializers.ModelSerializer):
  manager_details = ManagerProfileSerializer(source='manager', read_only=True)
  class Meta:
    model = models.AcademyTrainer
    fields = '__all__'


class AcademySubscribePlanSerializer(serializers.ModelSerializer):
  academy_details = AcademySerializer(source='academy', read_only=True)
  class Meta:
    model = models.AcademySubscribePlan
    fields = '__all__'













