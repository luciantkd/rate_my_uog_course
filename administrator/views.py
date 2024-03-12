from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse
from django.urls import reverse

from administrator.models import Admin
from lecturer.models import Course, Lecturer
from student.models import CourseFeedback
from rateMyUogCourse.models import WebsiteFeedback, CourseSearchTable


def mainPage(request):
    return HttpResponse("Main Page")


def reported_reviews_management(request):
    # get course feedbacks where reported != 0, and join with course names, and sort by reported
    course_feedbacks = CourseFeedback.objects.all().values('feedbackId', 'courseId', 'reported').filter(reported__gt=0)
    # search for course name, program type
    course_feedbacks_view = []
    for feedback in course_feedbacks:
        course = Course.objects.get(courseId=feedback['courseId'])
        course_feedbacks_view.append({
            'feedbackId': feedback['feedbackId'],
            'courseId': feedback['courseId'],
            'courseName': course.courseName,
            'programType': course.programType,
            'reported': feedback['reported'],
        })
    # print(course_feedbacks_view)
    return render(request, "administrator/reported_reviews_management.html", {'course_feedbacks': course_feedbacks_view})
    # return render(request, reverse('administrator:reported_reviews_management'), {'course_feedbacks': course_feedbacks})

    # return render(request, 'report_review_management.html')

# Admin - Reported Review Detail
# This method is to show the detail of a reported review
# @param feedback_id the id of the feedback
# @return: feedback_entity, course_name
def reported_review_detail(request):
    feedback_id = request.GET.get('feedback_id')
    feedback_entity = get_object_or_404(CourseFeedback, pk=feedback_id)
    # get the course name
    print(feedback_entity.courseId_id)
    course = Course.objects.get(courseId=feedback_entity.courseId_id)
    course_name = course.courseName
    # semester = course.semester
    return render(request, 'administrator/admin_report_review_detail.html',
                  {'feedback_entity': feedback_entity, 'course_name': course_name, })

# Admin - Delete Reported Review
# This method is to delete a reported review
# @param feedback_id: the id of the feedback
# @return: boolean success
def reported_review_approve(request, feedback_id):
    feedback_entity = get_object_or_404(CourseFeedback, pk=feedback_id)
    if feedback_entity is not None:
        feedback_entity.delete()
    return redirect(reverse('administrator:report_review_management'))

def reported_review_delete(request, feedback_id):
    print(feedback_id)
    feedback = get_object_or_404(CourseFeedback, feedbackId=feedback_id)
    feedback.reported = 0
    # print(feedback.feedbackDateTime)
    # feedback.feedbackDateTime = datetime.now()
    feedback.save()
    return redirect(reverse('administrator:report_review_management'))




def base(request):
    return render(request, 'administrator:course_management')

def logout(request):
    request.session.flush()
    return redirect(reverse('rateMyUogCourse:mainPage'))

# TODO: session check
def session_check(request):
    if request.session.get('user_type') != 'administrator':
        return redirect(reverse('rateMyUogCourse:login'))