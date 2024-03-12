from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from lecturer.models import Course
from student.models import Student, CourseFeedback


class CourseFeedbackViewTests(TestCase):
    def setUp(self):
        # Setup code here to create test records in the database
        self.client = Client()
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

    def test_main_page(self):
        response = self.client.get(reverse('mainPage'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Main Page")

    def test_reported_reviews_management(self):
        response = self.client.get(reverse('administrator:report_review_management'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('course_feedbacks' in response.context)

    def test_reported_review_detail(self):
        response = self.client.get(reverse('administrator:report_review_detail'), {'feedback_id': self.feedback.feedbackId})
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
