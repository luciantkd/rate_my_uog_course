from django.urls import path
from rateMyUogCourse import views


app_name = 'rateMyUogCourse'

urlpatterns = [
path('', views.mainPage, name='mainPage'),
path('login/', views.user_login, name='login'),
path('signup/', views.signup, name='signup'),
path('feedback/', views.feedback, name='feedback'),
path('searchCourses/<str:course_name>/<str:program_type>', views.search, name = 'search'),
path('test-base/', views.base_page, name='test_base'),
path('detail/', views.course_detail_page, name='course_detail')
]
