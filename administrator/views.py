from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from lecturer.models import Course
from student.models import CourseFeedback


def mainPage(request):
    """
    View function to display the main page.

    :param request: HttpRequest object.
    :return: HttpResponse object with the text "Main Page".
    """
    return HttpResponse("Main Page")


def reported_reviews_management(request):
    """
    View function to manage reported reviews. It fetches course feedbacks that have been reported, joins with course
    names, and sorts them by the reported count.

    :param request: HttpRequest object.
    :return: HttpResponse object rendering the 'reported_reviews_management' template with course feedbacks context.
    """
    course_feedbacks = CourseFeedback.objects.filter(reported__gt=0).values(
        'feedbackId', 'courseId', 'reported'
    )
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
    return render(request, "administrator/reported_reviews_management.html",
                  {'course_feedbacks': course_feedbacks_view})


def reported_review_detail(request):
    """
    View function to show the detail of a reported review by its feedback_id.

    :param request: HttpRequest object containing 'feedback_id' as a GET parameter.
    :return: HttpResponse object rendering the 'admin_report_review_detail' template with feedback entity and course name context.
    """
    feedback_id = request.GET.get('feedback_id')
    feedback_entity = get_object_or_404(CourseFeedback, pk=feedback_id)
    course = Course.objects.get(courseId=feedback_entity.courseId_id)
    course_name = course.courseName
    return render(request, 'administrator/admin_report_review_detail.html',
                  {'feedback_entity': feedback_entity, 'course_name': course_name})


def reported_review_approve(request, feedback_id):
    """
    View function to approve (effectively delete) a reported review identified by its feedback_id.

    :param request: HttpRequest object.
    :param feedback_id: The ID of the feedback to approve/delete.
    :return: HttpResponseRedirect object redirecting to the report review management view.
    """
    feedback_entity = get_object_or_404(CourseFeedback, pk=feedback_id)
    if feedback_entity:
        feedback_entity.delete()
    return redirect(reverse('administrator:report_review_management'))


def reported_review_delete(request, feedback_id):
    """
    View function to clear the reported status of a review by setting its 'reported' field to 0.

    :param request: HttpRequest object.
    :param feedback_id: The ID of the feedback whose reported status is to be cleared.
    :return: HttpResponseRedirect object redirecting to the report review management view.
    """
    feedback = get_object_or_404(CourseFeedback, feedbackId=feedback_id)
    feedback.reported = 0
    feedback.save()
    return redirect(reverse('administrator:report_review_management'))


def base(request):
    return render(request, 'administrator:course_management')


def logout(request):
    """
    View function to handle user logout by flushing the session.

    :param request: HttpRequest object.
    :return: HttpResponseRedirect object redirecting to the main page of 'rateMyUogCourse'.
    """
    request.session.flush()
    return redirect(reverse('rateMyUogCourse:mainPage'))
