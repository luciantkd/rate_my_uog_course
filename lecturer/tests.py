from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from lecturer.models import LecturerCourseAssignment, Lecturer
from rateMyUogCourse.models import CourseSearchTable
from student.models import Course
from lecturer.views import  lecturer_course_overview

# Create your tests here.

class LecturerCourseOverviewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_lecturer_course_overview(self):
        # Create a mock lecturer ID and associated course IDs
        lecturer_id = 123
        course_ids = [1, 2, 3]

        # Create mock Course objects
        courses = [
            Course.objects.create(courseId=course_id, courseName=f'Course {course_id}', semester = 1)
            for course_id in course_ids
        ]
        lecturer = Lecturer.objects.create(lecturerId = lecturer_id)
        # Create mock LecturerCourseAssignment objects
        lecturer_course_assignments = [
            LecturerCourseAssignment.objects.create(lecturerId = lecturer, courseId=courses[i])
            for i in range(len(course_ids))
        ]

        # Create a mock request
        request = self.factory.get(reverse('lecturer:course_overview', kwargs={'lecturerId': lecturer_id}))
        request.session = {'user_type': 'lecturer', 'user_id': lecturer_id}

        # Process the request
        response = lecturer_course_overview(request, lecturerId=lecturer_id)


        # Check response status code
        self.assertEqual(response.status_code, 200)

