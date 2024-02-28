from django import forms
from rateMyUogCourse.models import WebsiteFeedback

class WebsiteFeedback(forms.ModelForm):
    class Meta:
        model = WebsiteFeedback
        exclude = ['feedbackTime']
