from django.urls import path
from lecturer import views


app_name = 'lecturer'

urlpatterns =[

path('course_rating_overview/<str:lecturerId>', views.lecturer_course_overview, name='course_overview'),
]
