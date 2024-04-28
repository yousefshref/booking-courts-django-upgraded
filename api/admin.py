from django.contrib import admin
from .models import CustomUser, Court, Country, CourtType, City, State, Book,  PinnedTime, AcademyType, Academy, AcademyTime, AcademyTrainer, AcademySubscribePlan, UserProfile, StaffProfile, ManagerProfile, Setting, CourtFeature, CourtImage, CourtTool, CourtVideo, VerificationCode, WhiteList, Income, Expense, Subsribe



admin.site.register([CustomUser, Court, Country, CourtType, City, State, Book, PinnedTime, AcademyType, Academy, AcademyTime, AcademyTrainer, AcademySubscribePlan, UserProfile, StaffProfile, ManagerProfile, Setting, CourtFeature, CourtImage, CourtTool, CourtVideo, VerificationCode, WhiteList, Income, Expense, Subsribe])
