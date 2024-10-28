from django.urls import path

from administrator import views
from administrator.view import course_view
from administrator.view import feedback_view
from administrator.view import lecturer_view

app_name = 'administrator'

urlpatterns = [
    path('', views.mainPage, name='mainPage'),
    path('base/', views.base, name='base'),
    path('report_review_management/', views.reported_reviews_management, name='report_review_management'),
    path('report_review_detail/', views.reported_review_detail, name='report_review_detail'),
    path('reported_review_delete/<int:feedback_id>/', views.reported_review_delete, name='reported_review_delete'),
    path('reported_review_approve/<int:feedback_id>/', views.reported_review_approve, name='reported_review_approve'),
    # website feedback part
    path('website_feedback_management/', feedback_view.website_feedback_management, name='website_feedback_management'),
    path('website_feedback_detail/', feedback_view.website_feedback_detail, name='website_feedback_detail'),
    path('website_feedback_delete/', feedback_view.website_feedback_delete, name='website_feedback_delete'),
    # course part
    path('course_management/', course_view.course_management, name='course_management'),
    path('course_delete/', course_view.course_delete, name='course_delete'),
    path('course_edit/', course_view.course_edit, name='course_edit'),
    path('course_add/', course_view.course_add, name='course_add'),
    # Lecturer Part
    path('lecturer_management/', lecturer_view.lecturer_management, name='lecturer_management'),
    path('lecturer_edit/', lecturer_view.lecturer_edit, name='lecturer_edit'),
    path('lecturer_delete/', lecturer_view.lecturer_delete, name='lecturer_delete'),
    path('logout/', views.logout, name='logout')
]
