from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from lecturer.models import Course, Lecturer, LecturerCourseAssignment
from rateMyUogCourse.models import CourseSearchTable
from student.models import Student, CourseFeedback


class CourseFeedbackViewTests(TestCase):
    def setUp(self):
        # Setup code here to create test records in the database
        # admin login
        self.client = Client()
        session = self.client.session
        session['user_type'] = 'administrator'
        session.save()
        self.course = Course.objects.create(courseId="CSC101", courseName="Intro to CS", programType="CS",
                                            semester=2023)

        # Assuming you have a method to add students as provided
        self.student = Student.objects.create(guid="1234567", email="1234567t@student.gla.ac.uk", name="test_user_1",
                                              password="1qaz@WSX", programType="CS")

        self.feedback = CourseFeedback.objects.create(
            courseId=self.course,
            guid=self.student,
            overall=5,
            difficulty=3,
            usefulness=4,
            workload=3,
            examFormat="Multiple Choice",
            evaluationMethod="Exams and Projects",
            lecturerRating=4,
            gradeReceived="A",
            recommendCourse=True,
            textFeedback="Very informative course.",
            likes=0,
            reported=1,
            approved=False,
            feedbackDateTime=timezone.now()
        )

        self.search_table = CourseSearchTable.objects.create(
            courseId=self.course,
            courseName=self.course.courseName,
            overall=5,
            difficulty=3,
            usefulness=4,
            workload=3,
            reviews=1,
            wouldRecommend=1,
            professorRating=4
        )
        # Create some test data
        self.course1 = Course.objects.create(courseId="CS101", courseName="Intro to Computer Science", programType="CS",
                                             semester=2021)
        self.course2 = Course.objects.create(courseId="CS102", courseName="Data Structures", programType="CS",
                                             semester=2021)
        self.lecturer1 = Lecturer.objects.create(lecturerId="L001", lecturerName="Dr. Algorithm",
                                                 designation="Professor", email="algorithm@example.com",
                                                 password="securepassword")
        LecturerCourseAssignment.objects.create(courseId=self.course1, lecturerId=self.lecturer1)
        LecturerCourseAssignment.objects.create(courseId=self.course2, lecturerId=self.lecturer1)


    def test_reported_reviews_management(self):
        response = self.client.get(reverse('administrator:report_review_management'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('course_feedbacks' in response.context)

    def test_reported_review_detail(self):
        response = self.client.get(reverse('administrator:report_review_detail'),
                                   {'feedback_id': self.feedback.feedbackId})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.feedback.textFeedback)

    def test_reported_review_approve(self):
        response = self.client.post(reverse('administrator:reported_review_approve', args=[self.feedback.feedbackId]))
        self.assertEqual(response.status_code, 302)  # Redirect status
        self.assertFalse(CourseFeedback.objects.filter(feedbackId=self.feedback.feedbackId).exists())

    def test_reported_review_delete(self):
        response = self.client.post(reverse('administrator:reported_review_delete', args=[self.feedback.feedbackId]))
        self.assertEqual(response.status_code, 302)  # Redirect status
        updated_feedback = CourseFeedback.objects.get(feedbackId=self.feedback.feedbackId)
        self.assertEqual(updated_feedback.reported, 0)

    def test_course_management_with_filters(self):
        # Set the query parameters for program filter
        response = self.client.get(reverse('administrator:course_management'), {'program': 'CS'})
        self.assertEqual(response.status_code, 200)
        # Check if the response contains courses filtered by the CS program
        courses = response.context['courses']
        self.assertTrue(all(course['programType'] == 'CS' for course in courses))
        # Optionally, check for specific course names or IDs in the response

    def test_course_add_new(self):
        new_course_data = {
            'course_id': 'CS103',
            'course_name': 'Algorithms',
            'program_type': 'CS',
            'semester': '2022',
            'professor': 'Dr. Algorithm'
        }
        response = self.client.post(reverse('administrator:course_edit'), new_course_data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect to the course management page
        self.assertTrue(Course.objects.filter(courseId='CS103').exists())
        # Optionally, verify that the lecturer is also created/assigned

    def test_course_add_new(self):
        new_course_data = {
            'course_id': 'CS103',
            'course_name': 'Algorithms',
            'program_type': 'CS',
            'semester': '2022',
            'professor': 'Dr. Algorithm'
        }
        response = self.client.post(reverse('administrator:course_edit'), new_course_data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect to the course management page
        self.assertTrue(Course.objects.filter(courseId='CS103').exists())
        # Optionally, verify that the lecturer is also created/assigned

    def test_course_delete(self):
        # Assuming course1 is to be deleted
        response = self.client.post(reverse('administrator:course_delete'), {'course_id': self.course1.courseId})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after deletion
        self.assertFalse(Course.objects.filter(courseId=self.course1.courseId).exists())
