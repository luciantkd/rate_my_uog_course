import hashlib

import requests
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

from administrator.models import Admin
from lecturer.models import Course
from lecturer.models import Lecturer
from rateMyUogCourse.forms import WebsiteFeedback
from rateMyUogCourse.models import CourseSearchTable
from rate_my_uog_course.settings import RECAPTCHA_PRIVATE_KEY
from student.models import Student

#Home page of the Application
def mainPage(request):

    #Setting the session as visitor
    request.session['user_type'] = 'visitor'
    return render(request, 'rateMyUogCourse/homepage.html')


def checkPassword(inputPassword, userPassword):
    # check if the input password equals the user's password
    return hashlib.sha256(inputPassword.encode('utf-8')).hexdigest() == userPassword


def encryptPassword(password: str) -> str:
    """
    Encrypts a password using SHA-256 hashing algorithm.

    Parameters:
    password (str): The password to be encrypted.

    Returns:
    str: The hashed password.

    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def user_login(request):
    '''
    This is the google recaptcha v3 login function
    '''
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        print(result)
        # if the recaptcha is not valid
        if not result['success']:
            return render(request, 'rateMyUogCourse/login.html',
                          {'errorMessage': 'Invalid reCAPTCHA. Please try again.'})

        '''
            This is the original login function
        '''
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        #Check if the given email Id exists in student table
        if Student.objects.filter(email=email):
            user = Student.objects.filter(email=email)[0]

            #Check the password for authentication
            if checkPassword(password, user.password):

                #Set the session user type, id and email
                request.session['user_email'] = user.email
                request.session['user_type'] = 'student'
                request.session['user_id'] = user.guid

                #As it is successful login redirect them to student course overview  page
                return redirect('student:search')
            else:
                context_dict = {}
                # If password doesnt match we send this message, we dont send as password incorrect,
                # as if a attacker tries to login, they get to know that the email exists and only the password is wrong!
                context_dict['errorMessage'] = 'Invalid login details'
                return render(request, 'rateMyUogCourse/login.html', context_dict)

        ##Check if the given email Id exists in Lecturer table
        elif Lecturer.objects.filter(lecturerId=email.split('@')[0]):
            user = Lecturer.objects.get(lecturerId=email.split('@')[0])

            #Check the password for authentication
            if checkPassword(password, user.password):

                 #Set the session user type, id and email
                request.session['user_email'] = user.email
                request.session['user_type'] = 'lecturer'
                request.session['user_id'] = user.lecturerId

               #As it is successful login redirect them to lecturer course overview  page
                return redirect('lecturer:course_overview', lecturerId=user.lecturerId)
            else:
                context_dict = {}
                # If password doesnt match we send this message, we dont send as password incorrect,
                # as if a attacker tries to login, they get to know that the email exists and only the password is wrong!
                context_dict['errorMessage'] = 'Invalid login details'
                context_dict['errorMessage'] = 'Invalid login details'
                return render(request, 'rateMyUogCourse/login.html', context_dict)
            
        ##Check if the given email Id exists in Admin table
        elif Admin.objects.filter(email=email):
            user = Admin.objects.filter(email=email)[0]

            #Check the password for authentication
            if checkPassword(password, user.password):
                request.session['user_email'] = user.email
                request.session['user_type'] = 'administrator'

                #As it is successful login redirect them to Admin course management page
                return redirect(reverse('administrator:course_management'))
            else:
                context_dict = {}
                context_dict['errorMessage'] = 'Invalid login details'
                return render(request, 'rateMyUogCourse/login.html', context_dict)

        else:
            # If password doesnt match we send this message, we dont send as password incorrect,
            # as if a attacker tries to login, they get to know that the email exists and only the password is wrong!
            context_dict = {}
            context_dict['errorMessage'] = 'Invalid login details'

            return render(request, 'rateMyUogCourse/login.html', context_dict)

    return render(request, 'rateMyUogCourse/login.html')


def signup(request):
    # only Student can sign up from website

    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        print(result)
        # if the recaptcha is not valid
        if not result['success']:
            return render(request, 'rateMyUogCourse/signup.html',
                          {'errorMessage': 'Invalid reCAPTCHA. Please try again.'})

        '''
            This is the original signup function
        '''
        email = request.POST.get('email').lower()
        name = request.POST.get('name')
        password = request.POST.get('password')
        programType = request.POST.get('program_type')
        confirmPassword = request.POST.get('confirm_password')

        # check if the email is already signed up
        if Student.objects.filter(email=email):
            return HttpResponse('Already signed up')
        else:
            # check if the email is UofG student
            emailDomain = email.split("@")[1]
            if emailDomain != 'student.gla.ac.uk':
                return HttpResponse('Use UofG email to sign up.')

            # check if the password is the same
            if password == confirmPassword:

                guid = email.split("@")[0]
                # hash the password
                hashed_password = hashlib.sha256(password.encode('utf-8'))

                Student.objects.create(
                    guid=guid,
                    email=email,
                    name=name,
                    password=hashed_password.hexdigest(),
                    programType=programType,
                )
                return redirect(reverse('rateMyUogCourse:login'))

            else:
                # if the password is not the same as confirmPassword
                return render(request, 'rateMyUogCourse/signup.html')

    return render(request, 'rateMyUogCourse/signup.html')

#Function for rendering feedback page
def feedback(request):
    return render(request, 'rateMyUogCourse/feedbackPage.html')

# Search function for the course overview page
def search(request):
    course_name = request.POST.get('course_name')
    program_type = request.POST.get('program_type')
    context_dict = {}

    if bool(request.session):
        # Adding the user type and id to the context dictionary
        if request.session.get('user_type') == 'student':
            context_dict['user_type'] = 'student'
            context_dict['user_id'] = request.session.get('user_id')
        else:
            context_dict['user_type'] = 'visitor'
    search_results = CourseSearchTable.objects.all()

    #Filtering search based on the inputs from the user
    if (course_name == '' and (program_type == None or program_type == 'All')):
        search_results = CourseSearchTable.objects.all()

    else:
        try:
            if program_type != None and course_name != '':
                if program_type == 'All':
                    search_results = CourseSearchTable.objects.filter(courseName__icontains=course_name)
                else:
                    course_of_program_type = Course.objects.filter(programType=program_type) | Course.objects.filter(
                        programType='All')
                    course_name_list = [course.courseName for course in course_of_program_type]
                    course_filtered = [element for element in course_name_list if
                                       course_name.lower() in element.lower()]
                    search_results = CourseSearchTable.objects.filter(courseName__in=course_filtered)
            elif program_type != None and course_name == '':
                course_of_program_type = Course.objects.filter(programType=program_type) | Course.objects.filter(
                    programType='All')
                course_name_list = [course.courseName for course in course_of_program_type]
                search_results = CourseSearchTable.objects.filter(courseName__in=course_name_list)
            else:
                search_results = CourseSearchTable.objects.filter(courseName__icontains=course_name)


        except:
            print("Exception occured while performing search function")

    #Adding the final search results to the context dictionary
    context_dict['search_results'] = search_results

    return render(request, 'rateMyUogCourse/course_rating_overview.html', context=context_dict)


# For testing base.html
def base_page(request):
    return render(request, 'base.html')


#Function for saving the website feedback from any user
def save_website_feedback(request):
    if request.method == 'POST':
        form = WebsiteFeedback(request.POST)

        #check the if the form is valid, and save it!
        if form.is_valid():
            form.save()
            form_submitted = True
        else:
            return render(request, 'rateMyUogCourse/feedbackPage.html', {'form': form})
    else:
        form = WebsiteFeedback()

    return render(request, 'rateMyUogCourse/feedbackPage.html', {'form': form, 'form_submitted': form_submitted})

#Function for logout
def logout(request):

    #Flusing all the sessions stored
    request.session.flush()

    #Redirecting the user to main page
    return redirect(reverse('rateMyUogCourse:mainPage'))
