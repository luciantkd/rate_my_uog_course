from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse
from django.contrib import messages
from lecturer.models import Course, LecturerCourseAssignment, Lecturer
from rateMyUogCourse.models import CourseSearchTable


def course_management(request):
    program_filter = request.GET.get('program', '')
    query = request.GET.get('query', '')
    search_text = request.GET.get('search_text', '')
    courses_list = Course.objects.all().order_by('courseId')

    if program_filter:
        # add + in the program filter
        program_type = program_filter.replace(' ', '+')
        print(program_type)
        courses_list = courses_list.filter(programType=program_type)

    if query:
        # courses_list = courses_list.filter(courseName__icontains=query)
        # use Q object for complex queries, allowing search by both name and courseID
        courses_list = courses_list.filter(
            Q(courseName__icontains=query) |
            Q(courseId__icontains=query)
        ).order_by('courseId')



    print(courses_list)
    courses = []

    for course in courses_list:
        lecturer_names = course.lecturercourseassignment_set.all().values_list('lecturerId__lecturerName', flat=True)
        lecturer_names_str = ', '.join(lecturer_names)
        print(lecturer_names_str)

        courses.append({
            'courseId': course.courseId,
            'courseName': course.courseName,
            'programType': course.programType,
            'lecturerNames': lecturer_names_str,
            'search_text': search_text

        })

    # Check if it's an AJAX request
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse({'courses': courses}, safe=False)


    return render(request, 'administrator/course_management.html', {'courses': courses})


# Admin - Course Edit Page
def course_edit(request):
    '''
    This page is for the admin to add or edit course details.
    If a course_id is provided through GET, it edits the course, otherwise it handles adding a new course or the POST request of editing.
    :param request: the HTTP request.
    :return: rendered response.
    '''
    course_id = request.GET.get('course_id')
    if request.method == 'POST':
        # Retrieve and validate form data
        course_id = request.POST.get('course_id', '').strip()
        course_name = request.POST.get('course_name', '').strip()
        program_type = request.POST.get('program_type', '').strip()
        semester = request.POST.get('semester', '').strip()
        lecturer_names_input = request.POST.get('professor', '').strip()
        lecturer_names = [name.strip() for name in lecturer_names_input.split(',')] if lecturer_names_input else []
        if semester is None or semester == '':
            semester = 2023

        # Check if any field is missing
        if not (course_id and course_name and program_type and lecturer_names_input):
            messages.error(request, 'All fields must be filled out.')
            context = {
                'course': {
                    'courseId': course_id,
                    'courseName': course_name,
                    'programType': program_type,
                    'lecturerName': lecturer_names_input
                }
            }
            return render(request, 'administrator/course_edit.html', context)

        # Update or create the course
        course, created = Course.objects.update_or_create(
            courseId=course_id,
            defaults={'courseName': course_name, 'programType': program_type, 'semester': semester}
        )

        # Process lecturer names
        for lecturer_name in lecturer_names:
            try:
                lecturer = Lecturer.objects.get(lecturerName=lecturer_name)
                # LecturerCourseAssignment(lecturerId=lecturer, courseId=course).save()
            except Lecturer.DoesNotExist:
                messages.error(request, f'Lecturer "{lecturer_name}" not found. Please check the name and try again.')
                return render(request, 'administrator/course_edit.html', {
                    'course': {
                        'courseId': course_id,
                        'courseName': course_name,
                        'programType': program_type,
                        'lecturerName': lecturer_names_input
                    }
                })
        # Reset lecturer assignments for this course and process new lecturer names
        course.lecturercourseassignment_set.all().delete()
        for lecturer_name in lecturer_names:
            lecturer = Lecturer.objects.get(lecturerName=lecturer_name)
            LecturerCourseAssignment(lecturerId=lecturer, courseId=course).save()
        return redirect(reverse('administrator:course_management'))

    else:  # GET request for add or edit form
        course_data = {'courseId': '', 'courseName': '', 'programType': '', 'semester': '', 'lecturerName': ''}
        if course_id:
            course = get_object_or_404(Course, courseId=course_id)
            lecturer_names = course.lecturercourseassignment_set.all().values_list('lecturerId__lecturerName', flat=True)
            lecturer_names_str = ', '.join(lecturer_names)
            course_data = {
                'courseId': course.courseId,
                'courseName': course.courseName,
                'programType': course.programType,
                'semester': course.semester,
                'lecturerName': lecturer_names_str
            }

        return render(request, 'administrator/course_edit.html', {'course': course_data})



# Admin - Course Delete
# This method is to delete a course
# @param course_id: the id of the course
# @return: boolean success
def course_delete(request):
    if request.method == "POST":
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, pk=course_id)
        course.delete()
        return redirect(reverse('administrator:course_management'))  # Redirect to the course management page
    else:
        # Optionally handle the case for non-POST requests if necessary
        return redirect(reverse('administrator:course_management'))


# def course_edit(request):
#
#     return render(request, 'administrator/course_edit.html')
def course_add(request):
    return render(request, 'administrator/course_edit.html')
