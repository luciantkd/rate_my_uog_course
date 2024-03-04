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
    course_feedbacks = CourseFeedback.objects.all().values('course_id', 'courseId__courseName', 'review',
                                                           'reported').filter(reported__gt=0).order_by('reported')
    print(course_feedbacks)
    return render(request, 'administrator/reported_reviews_management.html', {'course_feedbacks': course_feedbacks})

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

    return render(request, 'administrator/feedback_management.html',
                  {'course_feedbacks': website_feedbacks, 'overall_avg': overall_avg, 'friendly_avg': friendly_avg,
                   'aesthetic_avg': aesthetic_avg})


# Admin - Website Feedback Review Detail
# This method is to show the detail of a feedback
# TODO: we need add one more attribute to the feedback, which is the feedback_id, right now we use feedback_time as
#  the id
# @param feedback_time the time of the feedback
# @return: feedback_entity
def website_feedback_detail(request):
    # get feedback time
    feedback_time = request.GET.get('feedback_time')
    # feedback_time is not a primary key
    feedback_entity_list = get_object_or_404(WebsiteFeedback, feedback_time=feedback_time)
    # get the first one
    feedback_entity = feedback_entity_list[0]
    return render(request, 'feedback_detail.html', {'feedback_entity': feedback_entity})


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

# Admin - Course Management
# This method is to show the course management page
# @return: courses a list of courses
def course_management(request):
    # courses = Course.objects.all()
    # course with lectrer name, and count of feedbacks
    courses = Course.objects.all().values('courseId', 'courseName', 'programType', 'semester', 'feedbackNum', 'lecturercourseassignment__lecturerId__lecturerName').order_by('courseId')
    return render(request, 'administrator/course_management.html', {'courses': courses})



# Admin - Course Detail Page
# This page is for the admin to edit the course details
# @param course_id: the id of the course
# @return: course
def course_detail(request):
    # print(request)
    course_id = request.GET.get('course_id')
    # get all
    course = get_object_or_404(Course, courseId=course_id)
    # print("course_detail is here: ")
    # print(course)
    return render(request, 'course_detail.html', {'course': course})


# Admin - Course Edit Post
# This method is to update or create a course, using post method
# @param request: the request
# @param course: an entity of course
# @return: boolean success
def course_edit_post(request):
    if (request.method == 'POST'):
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course_name')
        program_type = request.POST.get('program_type')
        # TODO: convert program type
        semester = request.POST.get('semester')
        course = Course(courseId=course_id, courseName=course_name, programType=program_type, semester=semester)
        course.save()
        # or redirect to the course management page
        return render(request, 'course_edit.html', {'success': True})


# Admin - Course Delete
# This method is to delete a course
# @param course_id: the id of the course
# @return: boolean success
def course_delete(request):
    if request.method == "POST":
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, pk=course_id)
        course.delete()
        return redirect(reverse('administrator:course_management'))  # Redirect to the course management page
    else:
        # Optionally handle the case for non-POST requests if necessary
        return redirect(reverse('administrator:course_management'))

def base(request):
    return render(request, 'administrator:course_management')

# View for testing viewing the Feedback Management page
# def feedback_management(request):
#     return render(request, 'administrator/feedback_management.html')

# View for testing viewing the Reported Reviews Management page
# def reported_reviews_management(request):
#     return render(request, 'administrator/reported_reviews_management.html')

# View for testing viewing the Lecturer Management page
def lecturer_management(request):
    # get lecturer list except passwords
    lecturers = Lecturer.objects.all().values('lecturerId', 'lecturerName', 'designation').order_by('lecturerId')
    return render(request, 'administrator/lecturer_management.html', {'lecturers': lecturers})

# def lecturer_management(request):


# TODO: session check
# def session_check(request):
