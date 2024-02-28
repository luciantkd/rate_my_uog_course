from django.shortcuts import render
from student.forms import StudentRegistrationForm
# Create your views here.
from django.http import HttpResponse


def mainPage(request):
 return HttpResponse("Main Page")
 
def register(request):

    registered = False
    
    if request.method == 'POST':
    
        registration_form = StudentRegistrationForm(request.POST)
        
        if registration_form.is_valid()
            student = registration_form.save()
            
            # not sure about how to confirm password
            student.set_password(user.password)
            student.save()
            
        else:
            print(registration_form..errors)
        
    else:
        registration_form = StudentRegistrationForm()
        
    
    return render(request, 'student/mainPage.html', context = {})