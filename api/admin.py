from django.contrib import admin
from .models import CustomUser, Court, Country, City, State, Book,  PinnedTime, AcademyType, Academy, AcademyTime, AcademyTrainer, AcademySubscribePlan,Invoice, UserProfile, StaffProfile, ManagerProfile, Setting, CourtFeature, CourtImage, CourtTool, CourtVideo, VerificationCode, WhiteList



admin.site.register([CustomUser, Court, Country, City, State, Book, PinnedTime, AcademyType, Academy, AcademyTime, AcademyTrainer, AcademySubscribePlan,Invoice, UserProfile, StaffProfile, ManagerProfile, Setting, CourtFeature, CourtImage, CourtTool, CourtVideo, VerificationCode, WhiteList])
