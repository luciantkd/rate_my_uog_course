from django.test import TestCase
from django.urls import reverse

import administrator.views as views
from django.test import TestCase, Client

from administrator.models import Admin
from lecturer.models import Course


# Create your tests here.
# urlpatterns = [
#     path ('', views.mainPage, name='mainPage'),
#     path ('report_review_management/', views.reported_reviews_management, name='report_review_management'),
#     path ('report_review_detail/', views.reported_review_detail, name='report_review_detail'),
#     path ('report_review_delete/', views.reported_review_delete, name='report_review_delete'),
#     path ('website_feedback_management/', views.website_feedback_management, name='website_feedback_management'),
#     path ('website_feedback_detail/', views.website_feedback_detail, name='website_feedback_detail'),
#     path ('website_feedback_delete/', views.website_feedback_delete, name='website_feedback_delete'),
#     path ('course_management/', views.course_management, name='course_management'),
#     path ('course_detail/', views.course_detail, name='course_detail'),
#     path ('course_edit_post/', views.course_edit_post, name='course_edit_post'),
#     path ('course_delete/', views.course_delete, name='course_delete'),
# ]

# urlpatterns = [
#     path ('', views.mainPage, name='mainPage'),
#     path ('report_review_management/', views.reported_reviews_management, name='report_review_management'),
#     path ('report_review_detail/', views.reported_review_detail, name='report_review_detail'),
#     path ('report_review_delete/', views.reported_review_delete, name='report_review_delete'),
#     path ('website_feedback_management/', views.website_feedback_management, name='website_feedback_management'),
#     path ('website_feedback_detail/', views.website_feedback_detail, name='website_feedback_detail'),
#     path ('website_feedback_delete/', views.website_feedback_delete, name='website_feedback_delete'),
#     path ('course_management/', views.course_management, name='course_management'),
#     path ('course_detail/', views.course_detail, name='course_detail'),
#     path ('course_edit_post/', views.course_edit_post, name='course_edit_post'),
#     path ('course_delete/', views.course_delete, name='course_delete'),
# ]
# python manage.py test administrator.tests.TestAdmin.unit_test


class TestAdmin(TestCase):
    def setUp(self):
        self.client = Client()
        Admin.objects.create(userName='admin1', password='admin1@example.com')
        # courses = [
        #     {'courseId': 'COMPSCI4039',
        #      'courseName': 'PROGRAMMING',
        #      'programType': 'IT+',
        #      'semester': 1},
        Course.objects.create(courseId='COMPSCI4039', courseName='PROGRAMMING', programType='IT+', semester=1)
    def unit_test(self):
        # construct a request object
        response = self.client.get(reverse('administrator:course_detail') + '?course_id=COMPSCI4039')
        print(response)
        # self.assertEqual(response.status_code, 404)
        # print(response)
        # views.course_detail('', "COMPSCI4039")
        # print(Admin.objects.all())