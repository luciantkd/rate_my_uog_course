from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from rateMyUogCourse.models import WebsiteFeedback


def website_feedback_management(request):
    # Retrieve all website feedback entries and select specific fields, ordered by feedbackId
    website_feedbacks = WebsiteFeedback.objects.all().values(
        'feedbackId', 'feedbackTime', 'friendly', 'overall', 'aesthetic'
    ).order_by('feedbackId')

    # Initialize average scores and count
    overall_avg = 0
    friendly_avg = 0
    aesthetic_avg = 0
    count = 0

    # If there are no feedback entries, render the management page with zero averages
    if len(website_feedbacks) == 0:
        return render(request, 'administrator/feedback_management.html', {
            'website_feedbacks': website_feedbacks,
            'overall_avg': overall_avg,
            'friendly_avg': friendly_avg,
            'aesthetic_avg': aesthetic_avg,
            'count': count
        })

    # Calculate the average scores for overall, friendly, and aesthetic feedback
    for feedback in website_feedbacks:
        overall_avg += feedback['overall']
        friendly_avg += feedback['friendly']
        aesthetic_avg += feedback['aesthetic']
        count += 1
    overall_avg /= count
    friendly_avg /= count
    aesthetic_avg /= count

    # Round the averages to 2 decimal places for display
    overall_avg = round(overall_avg, 2)
    friendly_avg = round(friendly_avg, 2)
    aesthetic_avg = round(aesthetic_avg, 2)

    # Render the feedback management page with the feedback entries and their average scores
    return render(request, 'administrator/feedback_management.html', {
        'website_feedbacks': website_feedbacks,
        'overall_avg': overall_avg,
        'friendly_avg': friendly_avg,
        'aesthetic_avg': aesthetic_avg,
        'count': count
    })


def website_feedback_detail(request):
    # Retrieve the feedback_id from the request's GET parameters
    feedback_id = request.GET.get('feedback_id')
    # Fetch the feedback entry with the given id or return a 404 error if not found
    feedback_entity = get_object_or_404(WebsiteFeedback, pk=int(feedback_id))

    # Prepare rating ranges for template rendering
    ratings = {
        'overall': range(feedback_entity.overall),
        'friendly': range(feedback_entity.friendly),
        'aesthetic': range(feedback_entity.aesthetic),
    }

    # Render the feedback detail page with the feedback entity and its ratings
    return render(request, 'administrator/feedback_detail.html', {
        'feedback_entity': feedback_entity,
        'ratings': ratings
    })


def website_feedback_delete(request):
    # Retrieve the feedback_id from the request's GET parameters
    feedback_id = request.GET.get('feedback_id')
    # Fetch the feedback entry with the given id or return a 404 error if not found
    feedback_entity = get_object_or_404(WebsiteFeedback, pk=feedback_id)

    # Delete the feedback entity
    feedback_entity.delete()

    # Redirect to the website feedback management page after deletion
    return redirect(reverse('administrator:website_feedback_management'))
