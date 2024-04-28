
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from api import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('whatsapp-send-verification/', views.send_whatsapp_message),

    path('signup-verification/', views.signup_send_verification),
    path('signup/', views.signup),
    path('login/', views.login),
    

    path('user/', views.user_detail),
    path('user/profile/', views.check_profile),


    path('user/manager/profile/create-or-update/', views.create_or_update_manager_profile),
    path('user/client/profile/create-or-update/', views.create_or_update_client_profile),

    path('countries/', views.countries_list),
    path('cities/<int:country_pk>/', views.cities_list),
    path('states/<int:city_pk>/', views.states_list),
    
    path('court-types/', views.courts_types_list),

    path('courts/', views.courts_list),
    path('court/<int:pk>/', views.court_detail),

    path('images/<int:court_id>/', views.images_list),
    path('image/<int:pk>/', views.image_detail),

    path('videos/<int:court_id>/', views.videos_list),
    path('video/<int:pk>/', views.video_detail),

    path('tools/<int:court_id>/', views.court_tools_list),
    path('tool/<int:pk>/', views.court_tool_detail),
    
    path('features/<int:court_id>/', views.court_features_list),
    path('feature/<int:pk>/', views.court_feature_detail),
    


    path('staffs/', views.staffs_list),
    path('staff/<int:pk>/', views.staff_detail),
    path('staff-user/<int:pk>/', views.staff_user_update),


    path('settings/', views.settings),


    path('book/check/<int:pk>/', views.court_detail_before_book),


    path('books/', views.books_list),
    path('book/<int:pk>/', views.book_detail),


    path('pinned-times/<int:book_id>/', views.pinned_list),
    path('pinned-time/<int:pinned_time_id>/', views.pinned_detail),


    path('academy-types/', views.academies_types),

    path('academies/', views.academies_list),
    path('academy/<int:pk>/', views.academy_detail),

    path('academy-times/', views.academy_times_list),
    path('academy-time/<int:pk>/', views.academy_time_detail),
    
    path('academy-subscribe-plans/', views.academy_subscribe_plans_list),
    path('academy-subscribe-plan/<int:pk>/', views.academy_subscribe_plan_detail),

    path('academy-trainers/', views.academy_trainers_list),
    path('academy-trainer/<int:pk>/', views.academy_trainer_detail),



    path('books/auto-cancel/', views.check_auto_cancell),



    path('white-lists/', views.white_list_list),
    path('white-list/<int:pk>/', views.white_list_detail),



    # get manager courts and academyes
    path('manager/<int:manager_id>/courts/', views.get_manager_courts),
    path('manager/<int:manager_id>/academies/', views.get_manager_academies),


    path('incomes/', views.incomes_list),
    path('income/<int:pk>/', views.income_detail),

    path('expenses/', views.expense_list),
    path('expense/<int:pk>/', views.expense_detail),


    path('subscriptions/', views.subscriptions_list),
    path('subscription/<int:pk>/', views.subscription_detail),


    path('test/', views.test),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
