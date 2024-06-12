from django.contrib import admin
from .models import CustomUser, Court, Country, CourtType, City, State, Book,  PinnedTime, AcademyType, Academy, AcademyTime, Trainer, AcademySubscribePlan, UserProfile, StaffProfile, ManagerProfile, Setting, CourtFeature, CourtImage, CourtCloseTime, Notification, CourtTool, CourtVideo, VerificationCode, WhiteList, Income, Expense, Subsribe, SubscriptionRenewal



admin.site.register([CustomUser, Court, Country, CourtType, City, State, Book, PinnedTime, AcademyType, Academy, AcademyTime, Trainer, AcademySubscribePlan, UserProfile, StaffProfile, ManagerProfile, Setting, CourtFeature, CourtImage, CourtCloseTime, Notification, CourtTool, CourtVideo, VerificationCode, WhiteList, Income, Expense, Subsribe, SubscriptionRenewal])
