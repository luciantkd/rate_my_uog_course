from django.urls import path
from administrator import views


app_name = 'administrator'

urlpatterns = [
path('', views.mainPage, name='mainPage'),
]
