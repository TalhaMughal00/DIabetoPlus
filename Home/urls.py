from django.contrib import admin
from django.urls import path
from Home import views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index , name='index'),
    # path('about/', views.about , name='about'),
    # path('prediction/', views.prediction , name='prediction'),
    # path('calculate_insulin/', views.calculate_insulin , name='calculate_insulin'),
    # path('new_diabetics/', views.new_diabtetics , name='new_diabetics'),
]