from django.urls import path
from lecturer import views


app_name = 'lecturer'

urlpatterns = [
path('', views.mainPage, name='mainPage'),
path('rateMyUogCourse/course_rating_overview', views.lecturer_course_overview, name = 'course_overview')
]
