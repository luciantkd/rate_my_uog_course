from django.shortcuts import render

from lecturer.models import LecturerCourseAssignment
from rateMyUogCourse.models import CourseSearchTable



# Returns the specific functions which the lecturer teaches for lecturer page
def lecturer_course_overview(request, lecturerId):

    context_dict = {}

    #Getting the user type and if from the session, which will be used in html pages

    context_dict['user_type'] = request.session.get('user_type')
    context_dict['user_id'] = request.session.get('user_id')

    #Fetching all the query sets from the lecturercourse relationship table, to get the coursesid

    lecturer_courses_id = LecturerCourseAssignment.objects.filter(lecturerId=lecturerId)

    #Collecting all the courseids in a list
    course_id_list = [each_lecturer.courseId for each_lecturer in lecturer_courses_id]

    #Getting all the courses from the serach table taught by the lecturer, using the course list
    lecturer_courses_overview = CourseSearchTable.objects.filter(courseId__in=course_id_list)

    #Adding the list to the final search_results, which will be used in html page
    context_dict['search_results'] = lecturer_courses_overview

    return render(request, 'rateMyUogCourse/course_rating_overview.html', context=context_dict)
