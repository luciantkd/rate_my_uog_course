from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from lecturer.models import LecturerCourseAssignment
from rateMyUogCourse.models import CourseSearchTable





def lecturer_course_overview(request, lecturerId):
 
 context_dict={}

 context_dict['user_type'] = request.session.get('user_type')
 context_dict['user_id'] = request.session.get('user_id')
 
 lecturer_courses_id = LecturerCourseAssignment.objects.filter(lecturerId=lecturerId)

 course_id_list = [each_lecturer.courseId for each_lecturer in lecturer_courses_id]

 lecturer_courses_overview = CourseSearchTable.objects.filter(courseId__in = course_id_list)

 context_dict['search_results'] = lecturer_courses_overview

 print(context_dict)

 return  render(request, 'rateMyUogCourse/course_rating_overview.html', context=context_dict)



