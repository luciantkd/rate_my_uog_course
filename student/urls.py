from django.urls import path

from rateMyUogCourse import views
from student import views as studentViews

app_name = 'student'

#Student related urls
urlpatterns = [
    path('detail/<str:course_Id>/<str:guId>', studentViews.show_detailed_rating, name='show_detailed_rating'),
    path('searchCourses', views.search, name='search'),
    path('save_feedback/<str:course_id>/<str:guId>', studentViews.save_feedback, name='save_feedback'),
    path('report_feedback/<int:feedback_id>/', studentViews.report_feedback, name='report_feedback'),
    path('like_feedback/<int:feedback_id>/<str:guId>', studentViews.like_feedback, name='like_feedback'),
]
