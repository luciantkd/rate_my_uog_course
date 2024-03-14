from django import forms

from rateMyUogCourse.models import WebsiteFeedback


# form for the website feedback
class WebsiteFeedback(forms.ModelForm):
    class Meta:
        model = WebsiteFeedback
        exclude = ['feedbackTime']
