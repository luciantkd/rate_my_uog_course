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
    course_feedbacks = CourseFeedback.objects.all().values('feedbackId', 'courseId', 'courseId__courseName', 'courseId__coursesearchtable__reviews',
                                                           'reported').filter(reported__gt=0).order_by('reported')
    print(course_feedbacks)
    return render(request, "administrator/reported_reviews_management.html", {'course_feedbacks': course_feedbacks})
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
    course_name = Course.objects.get(courseId=feedback_entity.courseId).courseName
    return render(request, 'report_review_detail.html',
                  {'feedback_entity': feedback_entity, 'course_name': course_name})

# Admin - Delete Reported Review
# This method is to delete a reported review
# @param feedback_id: the id of the feedback
# @return: boolean success
def reported_review_delete(request):
    feedback_id = request.GET.get('feedback_id')
    feedback_entity = get_object_or_404(CourseFeedback, pk=feedback_id)
    if feedback_entity is not None:
        feedback_entity.delete()
        return render(request, 'report_review_detail.html', {'success': True})
    else:
        return render(request, 'report_review_detail.html', {'success': False})




def base(request):
    return render(request, 'administrator:course_management')


# def lecturer_management(request):

def course_edit(request):
    return render(request, 'administrator/course_edit.html')

def create_course_management(request):
    return render(request, 'administrator/create_course_management.html')

def feedback_detail(request):
    return render(request, 'administrator/feedback_detail.html')

def lecturer_edit(request):
    return render(request, 'administrator/lecturer_edit.html')

def create_lecturer_account(request):
    return render(request, 'administrator/create_lecturer_account.html')

def admin_report_review_detail(request):
    return render(request, 'administrator/admin_report_review_detail.html')




# TODO: session check
# def session_check(request):
