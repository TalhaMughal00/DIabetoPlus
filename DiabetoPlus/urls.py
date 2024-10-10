"""
URL configuration for DiabetoPlus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Home import views as home_views
from predictor import views as predictor_views
from Glucose_Record import views as Glucose_Record_views
from recommendations import views as recommendations_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home_views.index , name='index'),
    path('about/', home_views.about , name='about'),
    # Feadback
    path('send_feedback/', home_views.send_feedback, name='send_feedback'),
    # Calculate Insulin
    path('calculate_insulin/', home_views.calculate_insulin , name='calculate_insulin'),
    # New Diabetics Info Page
    path('new_diabetics/', home_views.new_diabtetics , name='new_diabetics'),
    # User Login and SigUp
    path('login/', home_views.login_view, name='login'),
    path('sign_up/', home_views.sign_up, name='sign_up'),
    path('logout/', home_views.logout_view, name='logout'),
    path('change_password/', home_views.change_password, name='change_password'),
    # Prediction
    path('prediction/', predictor_views.predict_diabetes , name='predict_diabetes'),
    path('clear_predcition/',predictor_views.clear_prediction, name='clear_prediction'),
    # Records
    path('record/',Glucose_Record_views.record, name='record'),
    path('add_record/', Glucose_Record_views.add_record, name="add_record"),
    path('clear_records/', Glucose_Record_views.clear_records, name="clear_records"),
    path('delete_record/<int:pk>/', Glucose_Record_views.delete_record, name='delete_record'),
    path('record/update/<int:pk>/', Glucose_Record_views.update_record, name='update_record'),
    # PDF Generating
    path('gen_pdf/', Glucose_Record_views.gen_pdf, name='gen_pdf'),
    # Meal Planner
    path('mealplaner/', recommendations_views.meal_planner, name='mealplaner'),
    # Exercise Planner
    path('exercise/', recommendations_views.exercise_view, name='exercise'),
    # Profile Page
    path('profile/', home_views.profile, name="profile"),
    # Update Profile Picture
    path('profile/picture/', home_views.profile_pic, name='profile_pic'),
    # Reset Password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='pass_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='pass_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="pass_reset_confirm.html"), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="pass_reset_complete.html"), name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
