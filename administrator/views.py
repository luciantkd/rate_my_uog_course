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


def website_feedback_management(request):
    # get website feedbacks, sort by feedbackDateTime
    website_feedbacks = WebsiteFeedback.objects.all().values('feedbackTime', 'friendly', 'overall',
                                                             'aesthetic').order_by('feedbackTime')
    print(website_feedbacks)
    # count average of overall, friendly, aesthetic
    overall_avg = 0
    friendly_avg = 0
    aesthetic_avg = 0
    count = 0
    for feedback in website_feedbacks:
        overall_avg += feedback['overall']
        friendly_avg += feedback['friendly']
        aesthetic_avg += feedback['aesthetic']
        count += 1
    overall_avg = overall_avg / count
    friendly_avg = friendly_avg / count
    aesthetic_avg = aesthetic_avg / count

    print(website_feedbacks)

    return render(request, 'administrator/feedback_management.html',
                  {'website_feedbacks': website_feedbacks, 'overall_avg': overall_avg, 'friendly_avg': friendly_avg,
                   'aesthetic_avg': aesthetic_avg, 'count':count})


# Admin - Website Feedback Review Detail
# This method is to show the detail of a feedback
# TODO: we need add one more attribute to the feedback, which is the feedback_id, right now we use feedback_time as
#  the id
# @param feedback_time the time of the feedback
# @return: feedback_entity
def website_feedback_detail(request):
    # get feedback time
    feedback_time = request.GET.get('feedback_time')
    print(feedback_time)
    # feedback_time is not a primary key
    feedback_entity_list = get_object_or_404(WebsiteFeedback, feedback_time=feedback_time)
    # get the first one
    feedback_entity = feedback_entity_list[0]
    return render(request, 'administrator/feedback_detail.html', {'feedback_entity': feedback_entity})


# Admin - Delete Website Feedback
# This method is to delete a feedback
# @param feedback_time: the time of the feedback
# @return: boolean success
def website_feedback_delete(request):
    feedback_time = request.GET.get('feedback_time')
    feedback_entity = get_object_or_404(WebsiteFeedback, feedback_time=feedback_time)
    if feedback_entity is not None:
        feedback_entity.delete()
        return render(request, 'feedback_detail.html', {'success': True})
    else:
        return render(request, 'feedback_detail.html', {'success': False})






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
