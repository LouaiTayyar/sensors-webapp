from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('query_readings', views.query_readings, name='query_readings'),
    path('manage_readings', views.manage_readings, name='manage_readings'),
    path('manage_sensors', views.manage_sensors, name='manage_sensors'),
]