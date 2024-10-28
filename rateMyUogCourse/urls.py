from django.urls import path

from rateMyUogCourse import views

app_name = 'rateMyUogCourse'

#Common urls for all the users.
urlpatterns = [
    path('', views.mainPage, name='mainPage'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('feedback/', views.feedback, name='feedback'),
    path('searchCourses/', views.search, name='search'),
    path('test-base/', views.base_page, name='test_base'),
    path('logout/', views.logout, name='logout'),
    path('save_website_feedback/', views.save_website_feedback, name='save_website_feedback'),
]
