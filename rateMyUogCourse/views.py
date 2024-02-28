from django.shortcuts import render
from rateMyUogCourse.models import CourseSearchTable

from lecturer.models import Course

# Create your views here.
from django.http import HttpResponse


def mainPage(request):
 return render(request, 'rateMyUogCourse/homepage.html')


def login(request):
 return render(request, 'rateMyUogCourse/login.html')

def signup(request):
 return render(request, 'rateMyUogCourse/signup.html')

def feedback(request):
 return render(request, 'rateMyUogCourse/feedbackPage.html')


def search(request, course_name, program_type):

    context_dict={}
    search_results = None

    if(course_name == None and program_type == None):
        search_results =  CourseSearchTable.objects.all()
 
    try:
        course_of_program_type = Course.objects.get(programType = program_type)
        
        search_results = course_of_program_type.courseSearchTable_set.filter(string__contains=course_name )
    except:
        pass

    context_dict['search_results'] = search_results

    return  render(request, 'rateMyUogCourse/course_rating_overview.html', context=context_dict)




   


