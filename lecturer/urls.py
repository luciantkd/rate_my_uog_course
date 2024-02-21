from django.urls import path
from lecturer import views


app_name = 'lecturer'

urlpatterns = [
path('', views.mainPage, name='mainPage'),
]
