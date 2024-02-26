from django import forms
from student.models import Student

class StudentRegistrationForm(forms.ModelForm):
    guid = forms.CharField(max_length=7, )
    email = forms.EmailField(max_length=100, help_text = "Email Address")
    name = forms.CharField(max_length=200, help_text = "Name")
    password = forms.CharField(widget=forms.PasswordInput(), help_text = "Password")
    programType = forms.CharField(max_length=4, help_text = "Program Type")
    
    class Meta:
        model = Student
        fields = ('name', 'email', 'password', 'programType',)
    

    