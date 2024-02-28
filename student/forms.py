# forms.py
from django import forms
from student.models import CourseFeedback

class CourseFeedback(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        exclude = ['feedbackDateTime']
