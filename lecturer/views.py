from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from lecturer.models import LecturerCourseAssignment
from rateMyUogCourse.models import CourseSearchTable


def mainPage(request):
 return HttpResponse("Main Page")



def lecturer_course_overview(request, lecturer_id):
 
 context_dict={}
 
 lecturer_courses_id = LecturerCourseAssignment.objects.filter(lecturer_id)

 course_id_list = [lecturer_courses_id.courseId for each_lecturer in lecturer_courses_id]

 lecturer_courses_overview = CourseSearchTable.objects.filter(courseId__in = course_id_list)

 context_dict['search_results'] = lecturer_courses_overview

 return  render(request, 'rateMyUogCourse/course_rating_overview.html', context=context_dict)



