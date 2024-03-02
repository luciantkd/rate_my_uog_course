from django.urls import path
from administrator import views


app_name = 'administrator'

urlpatterns = [
path('', views.mainPage, name='mainPage'),
path('course_management/', views.course_management, name='course_management'),
path('base/', views.base, name='base'),
]
