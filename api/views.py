from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from bs4 import BeautifulSoup
import requests

from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.db.models import Q
import random

from django.core.cache import cache
from datetime import datetime, timedelta

from . import serializers
from . import models




def send_email(receiver_email, subject, message_body):
  # Email configuration
  sender_email = 'yb2005at@gmail.com'
  sender_password = 'ixvn wnfs airn gcqs'

  # Create message container
  msg = MIMEMultipart()
  msg['From'] = sender_email
  msg['To'] = receiver_email
  msg['Subject'] = subject

  # Attach message body
  msg.attach(MIMEText(message_body, 'plain'))

  # Connect to SMTP server
  smtp_server = smtplib.SMTP('smtp.gmail.com', 587)  # Change to your SMTP server and port
  smtp_server.starttls()  # Enable TLS encryption

  # Login to the SMTP server
  smtp_server.login(sender_email, sender_password)

  # Send email
  smtp_server.sendmail(sender_email, receiver_email, msg.as_string())

  # Close connection to SMTP server
  smtp_server.quit()

  return True



def verification_wahtsapp(phone_number):

  phone = phone_number

  verification = ''.join(str(random.randint(0, 9)) for _ in range(6))

  models.VerificationCode.objects.create(
      phone=phone,
      code=verification,
  )

  # http://198.204.228.117:8000/send_whatsapp_message/
  # requests.post('http://198.204.228.117:8000/send_whatsapp_message/?phone=${phone}&message=الكود هو ${verification} لا تشاركه مع احد', data={})
  
  
  requests.post('http://198.204.228.117:8000/send_whatsapp_message/', data={
    "phone": phone,
    "message": f"الكود هو {verification} لا تشاركه مع احد"
  })
  

  return Response({"success":True})



@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_whatsapp_message(request):
  phone = request.data.get('phone')

  verification = ''.join(str(random.randint(0, 9)) for _ in range(6))

  models.VerificationCode.objects.create(
      phone=phone,  
      code=verification,
  )
  
  requests.post('http://198.204.228.117:8000/send_whatsapp_message/', data={
    "phone": phone,
    "message": f"الكود هو {verification} لا تشاركه مع احد"
  })
  

  return Response({"success":True})


def send_whatsapp_message_function(phone, message):
  
  requests.post('http://198.204.228.117:8000/send_whatsapp_message/', data={
    "phone": f"{phone}",
    "message": f"{message}"
  })
  

  return Response({"success":True})




@api_view(['POST'])
def signup_send_verification(request):
  data = request.data.copy()
  data['username'] = data['username'].replace(" ", "_")
  serializer = serializers.UserSerializer(data=data)
  if serializer.is_valid():
    verification_wahtsapp(request.data['phone'])
    return Response({"success":True})
  return Response(serializer.errors)


@api_view(['POST'])
def signup(request):
  data = request.data.copy()
  data['username'] = data['username'].replace(" ", "_")
  serializer = serializers.UserSerializer(data=data)
  if serializer.is_valid():
    verificatio_code = models.VerificationCode.objects.filter(phone=request.data['phone']).last()
    

    if(str(data['phone']) == str(verificatio_code.phone) and str(data['verification']) == str(verificatio_code.code)):
      serializer.save() 
      user = models.CustomUser.objects.get(phone=request.data['phone'])
      user.set_password(request.data['password'])
      user.save()

      token = Token.objects.create(user=user)
      return Response({'token': token.key, 'user': serializer.data})
    else:
      return Response({'error': "البيانات خاطئة"})

  return Response(serializer.errors, status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
  user = models.CustomUser.objects.get(
    Q(phone=request.data['phone']) | Q(email=request.data['phone'])
  )
  if not user.check_password(request.data['password']):
    return Response("missing user", status=status.HTTP_404_NOT_FOUND)
  token, created = Token.objects.get_or_create(user=user)

  serializer = serializers.UserSerializer(user)
  return Response({'token': token.key, 'user': serializer.data})



def is_manager(request):
  try:
    manager_profile = models.ManagerProfile.objects.get(user=request.user)
    return manager_profile
  except:
    return False

def is_staff(request):
  try:
    staff_profile = models.StaffProfile.objects.get(user=request.user)
    return staff_profile
  except:
    return False




@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request):
  try:
    user = models.CustomUser.objects.get(pk=request.user.pk)
  except models.CustomUser.DoesNotExist:
    return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = serializers.UserSerializer(user)
    return Response(serializer.data)
  
  if request.method == 'PUT':
    serializer = serializers.UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'DELETE':
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_profile(request):
  
  if is_manager(request):
    manager_profile = models.ManagerProfile.objects.get(user=request.user)
    serializer = serializers.ManagerProfileSerializer(manager_profile)
    return Response({"manager": serializer.data})
  
  elif is_staff(request):
    staff_profile = models.StaffProfile.objects.get(user=request.user)
    serializer = serializers.StaffProfileSerializer(staff_profile)
    return Response({"staff": serializer.data})

  else:  
    user_profile = models.UserProfile.objects.get(user=request.user)
    serializer = serializers.UserProfileSerializer(user_profile)
    return Response({"user": serializer.data})



@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_manager_profile(request):

  if models.ManagerProfile.objects.filter(user=request.user).exists():
    return Response({"":""})
  
  data = request.data.copy()
  data['user'] = request.user.pk
  serializer = serializers.ManagerProfileSerializer(data=data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_client_profile(request):
  
  if models.UserProfile.objects.filter(user=request.user).exists():
    return Response({"":""})
  
  data = request.data.copy()
  data['user'] = request.user.pk
  serializer = serializers.UserProfileSerializer(data=data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def countries_list(request):
  countries = models.Country.objects.all()
  serializer = serializers.CitySerializer(countries, many=True)
  return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def cities_list(request, country_pk):
  cities = models.City.objects.filter(country=country_pk)
  serializer = serializers.CitySerializer(cities, many=True)
  return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def states_list(request, city_pk):
  states = models.State.objects.filter(city=city_pk)
  serializer = serializers.StateSerializer(states, many=True)
  return Response(serializer.data)


@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def courts_list(request):
  if request.method == 'GET':
    courts = models.Court.objects.filter(is_active=True).order_by('-id')

    if(is_manager(request)):
      courts = models.Court.objects.filter(manager=is_manager(request)).order_by('-id')

    if(is_staff(request)):
      courts = models.Court.objects.filter(manager=is_staff(request).manager).order_by('-id')
      
    if request.GET.get('country'):
      courts = courts.filter(country__id=request.GET.get('country'))

    if request.GET.get('city'):
      courts = courts.filter(city__id=request.GET.get('city'))

    if request.GET.get('state'):
      courts = courts.filter(state__id=request.GET.get('state'))
    

    if request.GET.get('name'):
      courts = courts.filter(name__icontains=request.GET.get('name'))


    serializer = serializers.CourtSerializer(courts, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    data = request.data.copy()

    if is_manager(request):
      data['manager'] = is_manager(request).pk
    
    if is_staff(request):
      data['manager'] = is_staff(request).manager.pk

    serializer = serializers.CourtSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def court_detail(request, pk):
  try:
    court = models.Court.objects.get(pk=pk)
  except models.Court.DoesNotExist:
    return Response({"error": "Court does not exist"}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
      serializer = serializers.CourtSerializer(court, context={'request': request})
      if request.GET.get('details'):
          total_money = 0
          total_books = 0
          all_court_books = models.Book.objects.filter(court=court)
          for i in all_court_books:
            total_money += i.total_price
            total_books += 1
          data = serializer.data
          data['total_money'] = total_money
          data['total_books'] = total_books
          return Response(data)
      return Response(serializer.data)
  
  if request.method == 'PUT':
    serializer = serializers.CourtSerializer(court, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'DELETE':
    court.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def images_list(request, court_id):
  if request.method == 'GET':
    image = models.CourtImage.objects.filter(court__pk=court_id)
    serializer = serializers.CourtImageSerializer(image, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    serializer = serializers.CourtImageSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def image_detail(request, pk):
  try:
    image = models.CourtImage.objects.get(pk=pk)
  except models.CourtImage.DoesNotExist:
    return Response({"error": "CourtImage does not exist"}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = serializers.CourtImageSerializer(image)
    return Response(serializer.data)
  
  if request.method == 'DELETE':
    image.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def videos_list(request, court_id):
  if request.method == 'GET':
    videos = models.CourtVideo.objects.filter(court__pk=court_id)
    serializer = serializers.CourtVideoSerializer(videos, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    serializer = serializers.CourtVideoSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def video_detail(request, pk):
  try:
    video = models.CourtVideo.objects.get(pk=pk)
  except models.CourtVideo.DoesNotExist:
    return Response({"error": "CourtImage does not exist"}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = serializers.CourtVideoSerializer(video)
    return Response(serializer.data)
  
  if request.method == 'DELETE':
    video.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def court_tools_list(request, court_id):
  if request.method == 'GET':
    tools = models.CourtTool.objects.filter(court__pk=court_id)
    serializer = serializers.CourtToolSerializer(tools, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    serializer = serializers.CourtToolSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def court_tool_detail(request, pk):
  try:
    tool = models.CourtTool.objects.get(pk=pk)
  except models.CourtTool.DoesNotExist:
    return Response({"error": "CourtImage does not exist"}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = serializers.CourtToolSerializer(tool)
    return Response(serializer.data)
  
  if request.method == 'PUT':
    instance = models.CourtTool.objects.get(pk=pk)
    serializer = serializers.CourtToolSerializer(instance, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)
  
  if request.method == 'DELETE':
    tool.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def court_features_list(request, court_id):
  if request.method == 'GET':
    features = models.CourtFeature.objects.filter(court__pk=court_id)
    serializer = serializers.CourtFeatureSerializer(features, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    serializer = serializers.CourtFeatureSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def court_feature_detail(request, pk):
  try:
    feature = models.CourtFeature.objects.get(pk=pk)
  except models.CourtFeature.DoesNotExist:
    return Response({"error": "CourtImage does not exist"}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = serializers.CourtFeatureSerializer(feature)
    return Response(serializer.data)
  
  if request.method == 'PUT':
    feature = models.CourtFeature.objects.get(pk=pk)
    serializer = serializers.CourtFeatureSerializer(feature, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'DELETE':
    feature.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)






@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def staffs_list(request):
  if request.method == 'GET':
    staffs = models.StaffProfile.objects.filter(manager=is_manager(request))
    serializer = serializers.StaffProfileSerializer(staffs, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    serializer = serializers.StaffProfileSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def staff_detail(request, pk):
  try:
    staff = models.StaffProfile.objects.get(pk=pk)
  except models.StaffProfile.DoesNotExist:
    return Response({"error": "StaffProfile does not exist"}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = serializers.StaffProfileSerializer(staff)
    return Response(serializer.data)
  
  if request.method == 'PUT':
    code_insance = models.VerificationCode.objects.filter(is_used=False, user=staff.user, email=request.data['email']).first()
    serializer = serializers.StaffProfileSerializer(data=request.data)
    if serializer.is_valid():
      if code_insance.code == request.data['code']:
        serializer.save()
        return Response(serializer.data)
      else:
        return Response({"error": "Verification code is not valid"})
    return Response(serializer.errors)
  
  if request.method == 'DELETE':
    staff.user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def staff_user_update(request, pk):
  try:
    staff_user = models.CustomUser.objects.get(pk=pk)
  except models.CustomUser.DoesNotExist:
    return Response({"error": "CustomUser does not exist"})
  
  if request.method == 'PUT':
    code_insance = models.VerificationCode.objects.filter(is_used=False, phone=request.data['phone']).last()
    user_instance = models.CustomUser.objects.get(pk=pk)
    print(code_insance.code)
    serializer = serializers.UserSerializer(user_instance, data=request.data, partial=True)
    if serializer.is_valid():
      if code_insance.code == request.data['code']:
        serializer.save()
        code_insance.is_used = True
        code_insance.save()
        return Response(serializer.data)
      else:
        return Response({"error": "Verification code is not valid"})
    return Response(serializer.errors)
  



# import pywhatkit as pwk
# import keyboard

# @api_view(['POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def vodafone_cash(request):
#   pwk.sendwhatmsg_instantly(request.GET.get('number'), request.GET.get('message'), 10, tab_close=True)
#   print("Message Sent!") #Prints success message in console
#   keyboard.press_and_release('ctrl+w')
#   return Response({"success":True})




@api_view(['GET', 'PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def settings(request):
  if request.method == 'GET':
    settings = models.Setting.objects.none()
    
    if is_manager(request):
      settings = models.Setting.objects.get(manager=is_manager(request))

    if is_staff(request):
      settings = models.Setting.objects.get(manager=is_staff(request).manager)
    
    if request.GET.get('manager_id'):
      settings = models.Setting.objects.get(manager__id=request.GET.get('manager_id'))

    serializer = serializers.SettingsSerializer(settings)
    return Response(serializer.data)
  
  if request.method == 'PUT':
    settings = models.Setting.objects.none()
    
    if is_manager(request):
      settings = models.Setting.objects.get(manager=is_manager(request))
    else:
      settings = models.Setting.objects.get(manager=is_staff(request).manager)

    serializer = serializers.SettingsSerializer(settings, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)



def generate_time_slots(start_time, end_time, slot_duration):
    slots = []
    current_time = start_time
    while current_time <= end_time:
        slots.append(current_time.strftime('%H:%M'))
        current_time += timedelta(minutes=slot_duration)
    return slots

def get_time_slots(start_time_str, end_time_str, slot_duration):
  start_time = datetime.strptime(start_time_str, '%H:%M')
  end_time = datetime.strptime(end_time_str, '%H:%M')
  
  # Case: Same times, return 24-hour slots
  if start_time == end_time:
    start_time = datetime.strptime('00:00', '%H:%M')
    end_time = datetime.strptime('23:59', '%H:%M')
    slots = generate_time_slots(start_time, end_time, slot_duration)
    return [f"{slots[i]}-{slots[i+1]}" for i in range(len(slots)-1)]

  # Case: Start time is greater than end time
  elif start_time > end_time:
    start_time, end_time = end_time, start_time

  slots = generate_time_slots(start_time, end_time, slot_duration)
  return [f"{slots[i]}-{slots[i+1]}" for i in range(len(slots)-1)]



def get_dates_between(start_date_str, end_date_str):
    # Convert input strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

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


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def court_detail_before_book(request, pk):
  try:
    court = models.Court.objects.get(pk=pk)
  except models.Court.DoesNotExist:
    return Response({"error": "Court does not exist"})

  # get slots of court oppening times
  slots = get_time_slots(str(court.open_from)[:5], str(court.open_to)[:5], 60)

  try:
    book = models.Book.objects.filter(court=court, is_cancelled=False)
  except:
    pass


  try:
    pinned = models.PinnedTime.objects.filter(date=request.GET.get('date'), is_cancelled=False)
  except Exception as e:
    pinned = []

  try:
    closed_slots = generate_time_slots(datetime.strptime(str(court.close_from)[:5], '%H:%M'), datetime.strptime(str(court.close_to)[:5], '%H:%M'), 60)
  except:
    closed_slots = []
 
  settings = models.Setting.objects.get(manager=court.manager)
  
  data = {
    "all_slots": slots,
    "closed_slots": closed_slots,
    "booked_slots": serializers.BookSerializer(book, many=True).data,
    "pinned": serializers.PinnedTimeSerializer(pinned, many=True).data,
    "court": serializers.CourtSerializer(court).data,
    "settings": serializers.SettingsSerializer(settings).data
  }

  return Response(data)


from django.utils.timezone import localtime
from datetime import timezone
@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def books_list(request):
  if request.method == 'GET':
    books = models.Book.objects.filter(user=request.user, is_cancelled=False)
    
    if is_manager(request):
      books = models.Book.objects.filter(court__manager=is_manager(request))

    if is_staff(request):
      books = models.Book.objects.filter(court__manager=is_staff(request).manager)


    if request.GET.get('date_from'):
      books = books.filter(date__gte=request.GET.get('date_from'))
      
    if request.GET.get('date_to'):
      books = books.filter(date__lte=request.GET.get('date_to'))
    
    if request.GET.get('court'):
      books = books.filter(court__id=request.GET.get('court'))

    if request.GET.get('is_cancelled'):
      books = books.filter(is_cancelled=request.GET.get('is_cancelled'))

    if request.GET.get('is_paied'):
      books = books.filter(is_paied=request.GET.get('is_paied'))

    if request.GET.get('paied'):
      books = books.filter(paied_with=request.GET.get('paied'))

    serializer = serializers.BookSerializer(books.order_by('-id'), many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    data = request.data.copy()
    serializer = serializers.BookSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_detail(request, pk):
  try:
    book = models.Book.objects.get(pk=pk)
  except models.Book.DoesNotExist:
    return Response({"error": "Book does not exist"})

  if request.method == 'GET':
    settings = models.Setting.objects.get(manager=book.court.manager)
    settings_ser = serializers.SettingsSerializer(settings)
    serializer = serializers.BookSerializer(book)

    # check if can be cancelled
    if request.GET.get('check_cancel'):
      can_cancel = False
      # get the created date
      created_date = localtime(book.created_at)
      print(created_date)
      # get the limit date
      limit = created_date + timedelta(minutes=settings_ser.data['limit_of_canceling_in_minuts'])
      print(limit)
      # get the current date
      current = localtime()
      print(current)
      # if current < limit -> can be cancelled
      if current < limit:
        can_cancel = True
      else:
        can_cancel = False
      
      if is_manager(request):
        can_cancel = True

    

    data = {
      "settings": settings_ser.data,
      "book": serializer.data,
      "can_cancel": can_cancel
    }
    return Response(data)
  
  if request.method == 'PUT':
    serializer = serializers.BookSerializer(book, data=request.data, partial=True)
    if serializer.is_valid():
      send_whatsapp_message_function(book.phone, f"لقد تم حجز الملعب {book.name} في تاريخ {book.date} الساعة {book.start_time} - {book.end_time}, يرجي الالتزام بالقوانين")
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)
  
  if request.method == 'DELETE':
    book.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)











@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def pinned_list(request, book_id):
  try:
    book = models.Book.objects.get(pk=book_id)
  except models.Book.DoesNotExist:
    return Response({"error": "Book does not exist"})

  pinned = models.PinnedTime.objects.filter(book=book, is_cancelled=False)
  
  if is_manager(request) or is_staff(request):
    pinned = models.PinnedTime.objects.filter(book=book)

  serializer = serializers.PinnedTimeSerializer(pinned, many=True)
  return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def pinned_detail(request, pinned_time_id):
  try:
    pinned = models.PinnedTime.objects.get(pk=pinned_time_id)
  except models.PinnedTime.DoesNotExist:
    return Response({"error": "Pinned does not exist"})

  if request.method == 'PUT':
    serializer = serializers.PinnedTimeSerializer(pinned, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)






@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def invoices_list(request):
  if request.method == 'GET':
    invoices = models.Invoice.objects.none()

    if is_manager(request):
      invoices = models.Invoice.objects.filter(manager=is_manager(request))

    if is_staff(request):
      invoices = models.Invoice.objects.filter(manager=is_staff(request).manager)

    if request.GET.get('created_at_start'):
      invoices = invoices.filter(created_at__gte=request.GET.get('created_at_start'))

    if request.GET.get('created_at_end'):
      invoices = invoices.filter(created_at__lte=request.GET.get('created_at_end'))

    if request.GET.get('only_courts'):
      invoices = invoices.filter(court__isnull=False)

    if request.GET.get('only_books'):
      invoices = invoices.filter(book__isnull=False)

    if request.GET.get('only_academies'):
      invoices = invoices.filter(academy__isnull=False)

    if request.GET.get('start_date'):
      invoices = invoices.filter(start_date=request.GET.get('start_date'))

    if request.GET.get('end_date'):
      invoices = invoices.filter(end_date=request.GET.get('end_date'))

    if request.GET.get('name'):
      invoices = invoices.filter(name__icontains=request.GET.get('name'))

    if request.GET.get('phone'):
      invoices = invoices.filter(phone__icontains=request.GET.get('phone'))

    if request.GET.get('book_id'):
      invoices = invoices.filter(book__id=request.GET.get('book_id'))

    if request.GET.get('court_id'):
      invoices = invoices.filter(court__id=request.GET.get('court_id'))
    
    if request.GET.get('academy_id'):
      invoices = invoices.filter(academy__id=request.GET.get('academy_id'))



    serializer = serializers.InvoiceSerializer(invoices.order_by('-id'), many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    data = request.data.copy()
    
    if is_manager(request):
      data['manager'] = is_manager(request).id 
    
    if is_staff(request):
      data['manager'] = is_staff(request).manager.id

    serializer = serializers.InvoiceSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)



@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def invoice_detail(request, pk):
  try:
    invoice = models.Invoice.objects.get(pk=pk)
  except models.Invoice.DoesNotExist:
    return Response({"error": "Invoice does not exist"})

  if request.method == 'GET':
    serializer = serializers.InvoiceSerializer(invoice)
    return Response(serializer.data)

  if request.method == 'PUT':
    serializer = serializers.InvoiceSerializer(invoice, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)

  if request.method == 'DELETE':
    invoice.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)







@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def academies_types(request):
  academy_types = models.AcademyType.objects.all()
  serializer = serializers.AcademyTypeSerializer(academy_types, many=True)
  return Response(serializer.data)




@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def academies_list(request):
  if request.method == 'GET':
    academies = models.Academy.objects.all()

    if is_manager(request):
      academies = models.Academy.objects.filter(manager=is_manager(request))

    if is_staff(request):
      academies = models.Academy.objects.filter(manager=is_staff(request).manager)

    if request.GET.get('name'):
      academies = academies.filter(name__icontains=request.GET.get('name'))

    if request.GET.get('type'):
      academies = academies.filter(type__pk=request.GET.get('type'))

    serializer = serializers.AcademySerializer(academies.order_by('-id'), many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    data = request.data.copy()

    if is_manager(request):
      data['manager'] = is_manager(request).pk

    if is_staff(request):
      data['manager'] = is_staff(request).manager.pk

    serializer = serializers.AcademySerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)



@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def academy_detail(request, pk):
  try:
    academy = models.Academy.objects.get(pk=pk)
  except models.Academy.DoesNotExist:
    return Response({"error": "Academy does not exist"})

  if request.method == 'GET':
    serializer = serializers.AcademySerializer(academy)
    return Response(serializer.data)

  if request.method == 'PUT':
    serializer = serializers.AcademySerializer(academy, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)

  if request.method == 'DELETE':
    academy.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)





@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def academy_times_list(request):
  if request.method == 'GET':
    academy_times = models.AcademyTime.objects.none()
    if(request.GET.get('academy_id')):
      academy_times = models.AcademyTime.objects.filter(academy__pk=request.GET.get('academy_id'))

    serializer = serializers.AcademyTimeSerializer(academy_times, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    data = request.data.copy()
    serializer = serializers.AcademyTimeSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)






@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def academy_time_detail(request, pk):
  try:
    academy_time = models.AcademyTime.objects.get(pk=pk)
  except models.AcademyTime.DoesNotExist:
    return Response({"error": "Academy Time does not exist"})

  if request.method == 'GET':
    serializer = serializers.AcademyTimeSerializer(academy_time)
    return Response(serializer.data)

  if request.method == 'PUT':
    serializer = serializers.AcademyTimeSerializer(academy_time, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)

  if request.method == 'DELETE':
    academy_time.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)








@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def academy_trainers_list(request):
  if request.method == 'GET':
    academy_trainers = models.AcademyTrainer.objects.all()

    if is_manager(request):
      academy_trainers = models.AcademyTrainer.objects.filter(manager=is_manager(request))
    
    if is_staff(request):
      academy_trainers = models.AcademyTrainer.objects.filter(manager=is_staff(request).manager)

    serializer = serializers.AcademyTrainerSerializer(academy_trainers.order_by('-id'), many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    data = request.data.copy()
    
    if is_manager(request):
      data['manager'] = is_manager(request).pk  
    
    if is_staff(request):
      data['manager'] = is_staff(request).manager.pk

    serializer = serializers.AcademyTrainerSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def academy_trainer_detail(request, pk):
  try:
    academy_trainer = models.AcademyTrainer.objects.get(pk=pk)
  except models.AcademyTrainer.DoesNotExist:
    return Response({"error": "Academy Trainer does not exist"})

  if request.method == 'GET':
    serializer = serializers.AcademyTrainerSerializer(academy_trainer)
    return Response(serializer.data)

  if request.method == 'PUT':
    serializer = serializers.AcademyTrainerSerializer(academy_trainer, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)

  if request.method == 'DELETE':
    academy_trainer.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)







@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def academy_subscribe_plans_list(request):
  if request.method == 'GET':
    academy_subscribe_plans = models.AcademySubscribePlan.objects.none()
    if request.GET.get('academy_id'):
      academy_subscribe_plans = models.AcademySubscribePlan.objects.filter(academy__pk=request.GET.get('academy_id'))
    serializer = serializers.AcademySubscribePlanSerializer(academy_subscribe_plans, many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    data = request.data.copy()
    serializer = serializers.AcademySubscribePlanSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def academy_subscribe_plan_detail(request, pk):
  try:
    academy_subscribe_plan = models.AcademySubscribePlan.objects.get(pk=pk)
  except models.AcademySubscribePlan.DoesNotExist:
    return Response({"error": "Academy Subscribe Plan does not exist"})

  if request.method == 'GET':
    serializer = serializers.AcademySubscribePlanSerializer(academy_subscribe_plan)
    return Response(serializer.data)

  if request.method == 'PUT':
    serializer = serializers.AcademySubscribePlanSerializer(academy_subscribe_plan, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)

  if request.method == 'DELETE':
    academy_subscribe_plan.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)









@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_auto_cancell(request):
  books = models.Book.objects.filter(is_cancelled=False, is_paied=False)

  todays_datetime = datetime.now()
  
  for book in books.all():
    
    settings = models.Setting.objects.get(manager=book.court.manager)

    if settings.limit_of_paying_in_minuts is not None and settings.limit_of_paying_in_minuts is not 0:

      book_created_date = book.created_at
      limites_in_minutes = settings.limit_of_paying_in_minuts

      limit_datetime = book_created_date + timedelta(minutes=limites_in_minutes)

      
      timestamp1_str = todays_datetime
      timestamp2_str = localtime(limit_datetime)

      # Parse strings into datetime objects
      timestamp1 = datetime.fromisoformat(str(timestamp1_str))
      timestamp2 = datetime.fromisoformat(str(timestamp2_str).split('+')[0])  # Removing timezone for compatibility

      user = book.user
      try:
        user_white_list = models.WhiteList.objects.get(user=user)
      except models.WhiteList.DoesNotExist:
        user_white_list = None
      
      if timestamp1 > timestamp2 and user_white_list is not None:
        book.is_cancelled = True
        if book.user.email:
          send_email(book.user.email, 'تم الغاء حجز بسبب عدم الدفع', f'تم الغاء حجز {book.court.name} بسبب عدم الدفع')
        book.save()
      else:
        pass

  return Response({"":""})



  


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def white_list_list(request):
  if request.method == 'GET':
    white_lists = models.WhiteList.objects.none()
    
    if is_manager(request):
      white_lists = models.WhiteList.objects.filter(manager=is_manager(request))

    if is_staff(request):
      white_lists = models.WhiteList.objects.filter(manager=is_staff(request).manager)

    serializer = serializers.WhiteListSerializer(white_lists.order_by('-id'), many=True)
    return Response(serializer.data)

  if request.method == 'POST':
    data = request.data.copy()

    user_exist = models.WhiteList.objects.none()

    try:
      user_exist = models.WhiteList.objects.get(phone=data['phone'])
      return Response({"خطأ": "هذا اللاعب يوجد بالفعل"})
    except:
      pass


    try:
      user = models.CustomUser.objects.get(phone=data['phone'])
    except:
      return Response({"خطأ": "لا يوجد لاعب بهذا الرقم"})


    data['user'] = user.pk

    if is_manager(request):
      data['manager'] = is_manager(request).pk

    if is_staff(request):
      data['manager'] = is_staff(request).manager.pk

    serializer = serializers.WhiteListSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)




@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def white_list_detail(request, pk):
  try:
    white_list = models.WhiteList.objects.get(pk=pk)
  except models.WhiteList.DoesNotExist:
    return Response({"error": "White List does not exist"})

  if request.method == 'GET':
    serializer = serializers.WhiteListSerializer(white_list)
    return Response(serializer.data)

  if request.method == 'PUT':
    data = request.data.copy()


    try:
      user = models.CustomUser.objects.get(phone=data['phone'])
    except:
      return Response({"خطأ": "لا يوجد لاعب بهذا الرقم"})

    
    serializer = serializers.WhiteListSerializer(white_list, data=data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors)

  if request.method == 'DELETE':
    white_list.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
















