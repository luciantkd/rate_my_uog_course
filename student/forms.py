# forms.py
from django import forms

from student.models import CourseFeedback


class CourseFeedback(forms.ModelForm):
    gradeReceived = forms.ChoiceField(choices=[('', '--Select an option--'),
                                               ('A', 'A'),
                                               ('B', 'B'),
                                               ('C', 'C'),
                                               ('D', 'D'),
                                               ('E', 'E'),
                                               ('F', 'F'),
                                               ('G', 'G'),
                                               ('H', 'H')], required=False)

    class Meta:
        model = CourseFeedback
        exclude = ['feedbackDateTime', 'likes', 'reported', 'approved']
