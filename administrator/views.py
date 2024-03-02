from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from lecturer.models import Course
from student.models import CourseFeedback
from rateMyUogCourse.models import WebsiteFeedback


def mainPage(request):
    return HttpResponse("Main Page")

def reported_reviews_management(request):
    # get course feedbacks where reported != 0, and join with course names, and sort by reported
    course_feedbacks = CourseFeedback.objects.all().values('course_id', 'courseId__courseName' ,'review', 'reported').filter(reported__gt=0).order_by('reported')
    print(course_feedbacks)
    return render(request, 'reported_reviews_management.html', {'course_feedbacks': course_feedbacks})

    # return render(request, 'report_review_management.html')

def feedback_management(request):
    # get website feedbacks, sort by feedbackDateTime
    website_feedbacks = WebsiteFeedback.objects.all().values('feedbackTime', 'friendly', 'overall', 'aesthetic').order_by('feedbackTime')
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

    return render(request, 'feedback_management.html', {'course_feedbacks': website_feedbacks, 'overall_avg': overall_avg, 'friendly_avg': friendly_avg, 'aesthetic_avg': aesthetic_avg})


def feedback_detail(request, feedback_id):
    feedback_entity = get_object_or_404(WebsiteFeedback, pk=feedback_id)
    return render(request, 'feedback_detail.html', {'feedback_entity': feedback_entity})

def report_review_detail(request, feedback_id):
    feedback_entity = get_object_or_404(CourseFeedback, pk=feedback_id)
    # get the course name
    course_name = Course.objects.get(courseId=feedback_entity.courseId).courseName
    return render(request, 'report_review_detail.html', {'feedback_entity': feedback_entity, 'course_name': course_name})

def course_management(request):
    return render(request, 'administrator/course_management.html')

def base(request):
    return render(request, 'administrator/base_admin.html')

def feedback_management(request):
    return render(request, 'administrator/feedback_management.html')

def reported_reviews_management(request):
    return render(request, 'administrator/reported_reviews_management.html')

# def lecturer_management(request):


# TODO: session check
# def session_check(request):

