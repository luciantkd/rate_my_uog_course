from django.urls import path
from rateMyUogCourse import views


app_name = 'rateMyUogCourse'

urlpatterns = [
path('login/', views.login, name='login'),
]
