from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.http import JsonResponse
import json

from student.views import save_feedback, show_detailed_rating, report_feedback, like_feedback
from student.models import Course, CourseFeedback, Student, StudentFeedbackLikes
from rateMyUogCourse.models import CourseSearchTable

class ShowDetailedRatingTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.student = Student.objects.create(guid='testid')
        self.course = Course.objects.create(courseId=1, courseName='123', semester = 1)
        self.course_feedback = CourseFeedback.objects.create(courseId=self.course, overall=4, difficulty=3,
                                                                     usefulness=4, workload=3,
                                                                     recommendCourse=True, lecturerRating=4, guid = self.student)
        self.courseSearchTable = CourseSearchTable.objects.create(courseId = self.course, courseName = self.course.courseName, 
        overall = 1, difficulty = 1, usefulness = 1, workload = 1, reviews = 1, wouldRecommend = True, professorRating = 1)


    def test_show_detailed_rating(self):
        url = reverse('student:show_detailed_rating', kwargs={'course_Id': self.course.courseId,
                                                      'guId': 'testid'})
        request = self.factory.get(url)
        request.session = {'user_type': 'student', 'user_id':self.student.guid}
        response = show_detailed_rating(request, self.course.courseId, 'testid')
        self.assertEqual(response.status_code, 200)


class ReportFeedbackTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.student = Student.objects.create(guid='testid')
        self.course = Course.objects.create(courseId=1, courseName='123', semester = 1)
        self.feedback = CourseFeedback.objects.create(courseId=self.course, overall=4, difficulty=3,
                                                             usefulness=4, workload=3,
                                                             recommendCourse=True, lecturerRating=4, guid = self.student)

    def test_report_feedback(self):
        url = reverse('student:report_feedback', kwargs={'feedback_id': self.feedback.feedbackId})
        request = self.factory.post(url)
        response = report_feedback(request, self.feedback.feedbackId)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, {'reported': True, 'reported_count': 1})



class LikeFeedbackTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.course = Course.objects.create(courseId=1, courseName='123', semester = 1)
        
        self.student = Student.objects.create(guid='testid')
        self.feedback = CourseFeedback.objects.create(courseId=self.course, overall=4, difficulty=3,
                                                             usefulness=4, workload=3,
                                                             recommendCourse=True, lecturerRating=4, guid = self.student)

    def test_like_feedback(self):
        url = reverse('student:like_feedback', kwargs={'feedback_id': self.feedback.feedbackId, 'guId': self.student.guid})
        request = self.factory.post(url)
        response = like_feedback(request, self.feedback.feedbackId, self.student.guid)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, {'success': True})

