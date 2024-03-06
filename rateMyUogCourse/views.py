from django.shortcuts import render, redirect, reverse
from rateMyUogCourse.models import CourseSearchTable

from lecturer.models import Course
from rateMyUogCourse.forms import WebsiteFeedback
from student.models import Student
from lecturer.models import Lecturer
from administrator.models import Admin
import hashlib

# Create your views here.
from django.http import HttpResponse


def mainPage(request):
 return render(request, 'rateMyUogCourse/homepage.html')
    
def checkPassword(inputPassword, userPassword):
    # check if the input password equals the user's password
    return hashlib.sha256(inputPassword.encode('utf-8')).hexdigest() == userPassword

def user_login(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')
        # user = Student.objects.filter(email = email)[0]
        
        if Student.objects.filter(email = email):
            user = Student.objects.filter(email = email)[0]
            if checkPassword(password, user.password):
                request.session['user_email'] = user.email
                request.session['user_type'] = 'student'
                request.session['user_id'] = user.guid
                # TODO: redirect to student page
                return redirect('rateMyUogCourse:search', course_name='None', program_type='None')
            else: 
                # TODO: change this into error context or pop up block
                return HttpResponse("Incorrect password")
            
        elif Lecturer.objects.filter(email = email):
            user = Lecturer.objects.filter(email = email)[0]
            if checkPassword(password, user.password):
                request.session['user_email'] = user.email
                request.session['user_type'] = 'lecturer'
                request.session['user_id'] = user.lecturerId
                # TODO: redirect to lecturer page
                return redirect(reverse('lecturer:course_overview'), lecturer_id = user.lecturerId)
            else: 
                # TODO: change this into error context or pop up block
                return HttpResponse("Incorrect password")
            
        elif Admin.objects.filter(email = email):
            user = Admin.objects.filter(email = email)[0]
            if checkPassword(password, user.password):
                request.session['user_email'] = user.email
                request.session['user_type'] = 'administrator'

                return redirect(reverse('administrator:course_management'))
            else: 
                # TODO: change this into error context or pop up block
                return HttpResponse("Incorrect password")
            
        else:
            # TODO: change this into error context or pop up block
            return HttpResponse('Invalid login details')

    return render(request, 'rateMyUogCourse/login.html')

 
def signup(request):
    # only Student can sign up from website

    if request.method == 'POST':

        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        programType = request.POST.get('program_type')
        confirmPassword = request.POST.get('confirm_password')
        
        # check if the email is already signed update
        if Student.objects.filter(email=email):
            return HttpResponse('Already signed up')
        else:
            # check if the email is UofG student
            emailDomain = email.split("@")[1]
            if emailDomain != 'student.gla.ac.uk':
                return HttpResponse('You are not a student of UofG.')
            
            # check if the password is the same
            if password == confirmPassword:
            
                guid = email.split("@")[0]
                # hash the password
                hashed_password = hashlib.sha256(password.encode('utf-8'))

                Student.objects.create(
                    guid = guid,
                    email = email,
                    name = name,
                    password = hashed_password.hexdigest(),
                    programType = programType,
                )
                return redirect(reverse('rateMyUogCourse:login'))
                
            else:
                # if the password is not the same as confirmPassword
                # TODO: change this into error context or pop up block
                return render(request, 'rateMyUogCourse/signup.html')

    return render(request, 'rateMyUogCourse/signup.html') 
 

def feedback(request):
 return render(request, 'rateMyUogCourse/feedbackPage.html')


def search(request, course_name, program_type):

    context_dict={}
    search_results = None

    if(course_name == 'None' and program_type == 'None'):
        search_results =  CourseSearchTable.objects.all()

    else:
 
        try:
            if program_type != 'None':
                course_of_program_type = Course.objects.filter(programType = program_type)
                course_name = [course.courseName for course in course_of_program_type]
                if course_name != 'None':
                    search_results = CourseSearchTable.objects.filter(courseName__in = course_name)

                else:
                    search_results = course_of_program_type
            else:
                search_results = CourseSearchTable.objects.filter(courseName=course_name )
            
        except:
            pass

    context_dict['search_results'] = search_results

    return  render(request, 'rateMyUogCourse/course_rating_overview.html', context=context_dict)

#For testing base.html
def base_page(request):
    return render(request,'base.html')


def save_website_feedback(request):
    if request.method == 'POST':
        form = WebsiteFeedback(request.POST)
        if form.is_valid():
            form.save()

    print('Website feedback saved successfully.')

def course_detail_page(request):
   return render(request, 'student/course_detail.html')
   


