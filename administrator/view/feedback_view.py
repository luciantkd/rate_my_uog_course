from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse

from rateMyUogCourse.models import WebsiteFeedback

def website_feedback_management(request):
    # get website feedbacks, sort by feedbackDateTime
    website_feedbacks = WebsiteFeedback.objects.all().values('feedbackId', 'feedbackTime', 'friendly', 'overall',
                                                             'aesthetic').order_by('feedbackId')
    # print(website_feedbacks)
    # count average of overall, friendly, aesthetic
    overall_avg = 0
    friendly_avg = 0
    aesthetic_avg = 0
    count = 0
    # if there is no feedback, return empty
    if len(website_feedbacks) == 0:
        return render(request, 'administrator/feedback_management.html', {'website_feedbacks': website_feedbacks, 'overall_avg': overall_avg, 'friendly_avg': friendly_avg,
                   'aesthetic_avg': aesthetic_avg, 'count':count})
    for feedback in website_feedbacks:
        overall_avg += feedback['overall']
        friendly_avg += feedback['friendly']
        aesthetic_avg += feedback['aesthetic']
        count += 1
    overall_avg = overall_avg / count
    friendly_avg = friendly_avg / count
    aesthetic_avg = aesthetic_avg / count
    # keep 2 decimal places
    overall_avg = round(overall_avg, 2)
    friendly_avg = round(friendly_avg, 2)
    aesthetic_avg = round(aesthetic_avg, 2)

    print(website_feedbacks)

    return render(request, 'administrator/feedback_management.html',
                  {'website_feedbacks': website_feedbacks, 'overall_avg': overall_avg, 'friendly_avg': friendly_avg,
                   'aesthetic_avg': aesthetic_avg, 'count':count})


# Admin - Website Feedback Review Detail
# This method is to show the detail of a feedback
# @param feedback_time the time of the feedback
# @return: feedback_entity
def website_feedback_detail(request):
    # get feedback time
    feedback_id = request.GET.get('feedback_id')
    print(feedback_id)
    feedback_entity = get_object_or_404(WebsiteFeedback, pk=int(feedback_id))
    print(str(feedback_entity))
    ratings = {
        'overall': range(feedback_entity.overall),
        'friendly': range(feedback_entity.friendly),
        'aesthetic': range(feedback_entity.aesthetic),
    }
    # get the first one
    return render(request, 'administrator/feedback_detail.html', {'feedback_entity': feedback_entity, 'ratings': ratings})


# Admin - Delete Website Feedback
# This method is to delete a feedback
# @param feedback_time: the time of the feedback
# @return: boolean success
def website_feedback_delete(request):
    feedback_id = request.GET.get('feedback_id')
    feedback_entity = get_object_or_404(WebsiteFeedback, pk=feedback_id)
    if feedback_entity is not None:
        feedback_entity.delete()
        return redirect(reverse('administrator:website_feedback_management'))

