from django.urls import path
from administrator import views


app_name = 'administrator'

urlpatterns = [
path('', views.mainPage, name='mainPage'),
path('course_management/', views.course_management, name='course_management'),
path('base/', views.base, name='base'),
path('feedback_management/', views.feedback_management, name='feedback_management'),
path('reported_reviews_management/', views.reported_reviews_management, name='reported_reviews_management'),
]
