from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils import timezone
from rateMyUogCourse.views import user_login, encryptPassword
from lecturer.models import Course, Lecturer, LecturerCourseAssignment
from student.models import Student, CourseFeedback
from administrator.models import Admin
from unittest.mock import MagicMock, patch

# Create your tests here.
class UserLoginTestCase(TestCase):
    def setUp(self):
        
        self.factory = RequestFactory()
        self.student_user_data = {
            'g-recaptcha-response': 'valid_token',
            'email': 'student@test.com',
            'password': 'testpassword'
        }
        self.lecturer_user_data = {
            'g-recaptcha-response': 'valid_token',
            'email': 'lecturer@test.com',
            'password': 'testpassword'
        }
        self.admin_user_data = {
            'g-recaptcha-response': 'valid_token',
            'email': 'admin@test.com',
            'password': 'testpassword'
        }
        # Create a user for each role
        self.student = Student.objects.create(email=self.student_user_data['email'], password=encryptPassword(self.student_user_data['password']))
        self.lecturer = Lecturer.objects.create(lecturerId = self.lecturer_user_data['email'].split('@')[0],email=self.lecturer_user_data['email'], password=encryptPassword(self.lecturer_user_data['password']))
        self.admin = Admin.objects.create(email=self.admin_user_data['email'], password=encryptPassword(self.admin_user_data['password']))

    def test_login_page_render(self):
        # Test rendering of login page

        request = self.factory.post(reverse('rateMyUogCourse:login'))
        response = user_login(request)
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'rateMyUogCourse/login.html')
        
    @patch('rateMyUogCourse.views.requests.post')
    def test_user_login_student(self, mock_post):
        # Test login as student
        mock_response = MagicMock()
        mock_response.json.return_value = {'success': True}
        mock_post.return_value = mock_response
        
        request = self.factory.post(reverse('rateMyUogCourse:login'), data=self.student_user_data)
        request.session = {}
        response = user_login(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(request.session['user_type'], 'student')
        
    @patch('rateMyUogCourse.views.requests.post')
    def test_user_login_lecturer(self, mock_post):
        # Test login as lecturer
        mock_response = MagicMock()
        mock_response.json.return_value = {'success': True}
        mock_post.return_value = mock_response
        
        request = self.factory.post(reverse('rateMyUogCourse:login'), data=self.lecturer_user_data)
        request.session = {}
        response = user_login(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(request.session['user_type'], 'lecturer')
        
    @patch('rateMyUogCourse.views.requests.post')
    def test_user_login_admin(self, mock_post):
        # Test login as admin
        mock_response = MagicMock()
        mock_response.json.return_value = {'success': True}
        mock_post.return_value = mock_response
        
        request = self.factory.post(reverse('rateMyUogCourse:login'), data=self.admin_user_data)
        request.session = {}
        response = user_login(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(request.session['user_type'], 'administrator')
