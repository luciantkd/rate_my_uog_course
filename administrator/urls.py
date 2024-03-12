from django.urls import path
from administrator import views
from administrator.view import lecturer_view
from administrator.view import course_view
from administrator.view import feedback_view
app_name = 'administrator'

urlpatterns = [
    path ('', views.mainPage, name='mainPage'),
    path ('base/', views.base, name='base'),
    path ('report_review_management/', views.reported_reviews_management, name='report_review_management'),
    path ('report_review_detail/', views.reported_review_detail, name='report_review_detail'),
    path('reported_review_delete/<int:feedback_id>/', views.reported_review_delete, name='reported_review_delete'),
    path('reported_review_approve/<int:feedback_id>/', views.reported_review_approve, name='reported_review_approve'),
    # website feedback part
    path ('website_feedback_management/', feedback_view.website_feedback_management, name='website_feedback_management'),
    path ('website_feedback_detail/', feedback_view.website_feedback_detail, name='website_feedback_detail'),
    path ('website_feedback_delete/', feedback_view.website_feedback_delete, name='website_feedback_delete'),
    # course part
    path ('course_management/', course_view.course_management, name='course_management'),
    # path ('course_edit_post/', course_view.course_edit_post, name='course_edit_post'),
    path ('course_delete/', course_view.course_delete, name='course_delete'),
    path ('course_edit/', course_view.course_edit, name='course_edit'),
    path ('course_add/', course_view.course_add, name='course_add'),
    # path ('course_add_post/', course_view.course_add_post, name='course_add_post'),
    # path ('create_course_management/', views.create_course_management, name='create_course_management'),
    # path ('feedback_detail/', views.feedback_detail, name='feedback_detail'),
    # Lecturer Part
    path ('lecturer_management/', lecturer_view.lecturer_management, name='lecturer_management'),
    path ('lecturer_edit/', lecturer_view.lecturer_edit, name='lecturer_edit'),
    # path ('lecturer_save_post/', lecturer_view.lecturer_save_post, name='lecturer_save_post'),
    path ('lecturer_delete/', lecturer_view.lecturer_delete, name='lecturer_delete'),
    # path ('lecturer_add/', lecturer_view.lecturer_add, name='lecturer_add'),
    # path ('lecturer_add_post/', lecturer_view.lecturer_add_post, name='lecturer_add_post'),
    # path ('create_lecturer_account/', views.create_lecturer_account, name='create_lecturer_account'),
    # path ('admin_report_review_detail/', views.admin_report_review_detail, name='admin_report_review_detail'),
]
