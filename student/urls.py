from django.urls import path
from student import views as studentViews
from rateMyUogCourse import views


app_name = 'student'

urlpatterns = [
    path('detail/<str:course_Id>/<str:guId>', studentViews.show_detailed_rating, name='show_detailed_rating'),
    path('searchCourses', views.search, name = 'search'),
    path('save_feedback/<str:course_id>/<str:guId>',studentViews.save_feedback, name = 'save_feedback')
    
]