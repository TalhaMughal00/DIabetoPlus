from django.contrib import admin
from django.urls import path
from Home import views
from predictor import views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index , name='index'),
]