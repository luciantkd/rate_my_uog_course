from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from lecturer.models import Course, LecturerCourseAssignment, Lecturer
from rateMyUogCourse.models import CourseSearchTable


def course_management(request):
    """
    Displays the course management page with a list of courses that can be filtered by program or searched by course
    name or ID.
    Supports AJAX requests for dynamic content loading.

    :param request: HttpRequest object containing GET parameters for 'program', 'query', and 'search_text'.
    :return: HttpResponse object rendering the course management page with context data for courses.
    """
    program_filter = request.GET.get('program', '')
    query = request.GET.get('query', '')
    search_text = request.GET.get('search_text', '')
    courses_list = Course.objects.all().order_by('courseId')

    if program_filter:
        program_type = program_filter.replace(' ', '+')
        courses_list = courses_list.filter(programType=program_type)

    if query:
        courses_list = courses_list.filter(
            Q(courseName__icontains=query) |
            Q(courseId__icontains=query)
        ).order_by('courseId')

    courses = [
        {
            'courseId': course.courseId,
            'courseName': course.courseName,
            'programType': course.programType,
            'lecturerNames': ', '.join(
                course.lecturercourseassignment_set.all().values_list('lecturerId__lecturerName', flat=True)),
            'reviews': 0,
            'search_text': search_text
        }
        for course in courses_list
    ]
    # append review
    for course in courses:
        if CourseSearchTable.objects.filter(courseId=course['courseId']).exists():
            course_search_table = CourseSearchTable.objects.get(courseId=course['courseId'])
            course['reviews'] = course_search_table.reviews
            print("course['reviews']", course['reviews'])


    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse({'courses': courses}, safe=False)

    return render(request, 'administrator/course_management.html', {'courses': courses})


def course_edit(request):
    """
    Handles both adding a new course and editing an existing course. If a course_id is provided via GET, it fetches the
    course for editing. POST requests handle the form submission for both adding and editing courses.

    :param request: HttpRequest object.
    :return: HttpResponse object. Redirects to the course management page on successful form submission or renders the
    course edit page with context data for form errors or initial data.
    """
    course_id = request.GET.get('course_id')
    if request.method == 'POST':
        course_id = request.POST.get('course_id', '').strip()
        course_name = request.POST.get('course_name', '').strip()
        program_type = request.POST.get('program_type', '').strip()
        semester = request.POST.get('semester', '').strip()
        lecturer_names_input = request.POST.get('professor', '').strip()

        if semester == '':
            semester = 2023

        if not (course_id and course_name and program_type and lecturer_names_input):
            messages.error(request, 'All fields must be filled out.')
            return render(request, 'administrator/course_edit.html', {
                'course': {
                    'courseId': course_id,
                    'courseName': course_name,
                    'programType': program_type,
                    'lecturerName': lecturer_names_input
                }
            })

        course, created = Course.objects.update_or_create(
            courseId=course_id,
            defaults={'courseName': course_name, 'programType': program_type, 'semester': semester}
        )

        # Reset and update lecturer assignments for the course
        course.lecturercourseassignment_set.all().delete()
        lecturer_names = [name.strip() for name in lecturer_names_input.split(',') if name.strip()]
        not_found_lecturers = []

        for lecturer_name in lecturer_names:
            if not Lecturer.objects.filter(lecturerName=lecturer_name).exists():
                not_found_lecturers.append(lecturer_name)

        if not_found_lecturers:
            messages.error(request, 'Lecturer not found: ' + ', '.join(not_found_lecturers))
            return render(request, 'administrator/course_edit.html', {
                'course': {
                    'courseId': course_id,
                    'courseName': course_name,
                    'programType': program_type,
                    'lecturerName': lecturer_names_input
                }
            })

        for lecturer_name in lecturer_names:
            lecturer = Lecturer.objects.get(lecturerName=lecturer_name)
            LecturerCourseAssignment.objects.create(lecturerId=lecturer, courseId=course)

        # search table, if exists, update, else create
        if CourseSearchTable.objects.filter(courseId=course).exists():
            course_search_table = CourseSearchTable.objects.get(courseId=course)
            course_search_table.courseName = course_name
            course_search_table.save()
        else:
            CourseSearchTable.objects.create(
                courseId=course,
                courseName=course_name,
                overall=0,
                difficulty=0,
                usefulness=0,
                workload=0,
                reviews=0,
                wouldRecommend=0,
                professorRating=0
            )
        return redirect(reverse('administrator:course_management'))
    else:
        course_data = {}
        if course_id:
            course = get_object_or_404(Course, courseId=course_id)
            course_data = {
                'courseId': course.courseId,
                'courseName': course.courseName,
                'programType': course.programType,
                'semester': course.semester,
                'lecturerName': ', '.join(
                    course.lecturercourseassignment_set.all().values_list('lecturerId__lecturerName', flat=True))
            }

        return render(request, 'administrator/course_edit.html', {'course': course_data})


def course_delete(request):
    """
    Deletes a course identified by the 'course_id' POST parameter and redirects to the course management page.

    :param request: HttpRequest object containing 'course_id' as a POST parameter.
    :return: HttpResponseRedirect object redirecting to the course management view.
    """
    if request.method == "POST":
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, pk=course_id)
        course.delete()
        return redirect(reverse('administrator:course_management'))
    else:
        return redirect(reverse('administrator:course_management'))


def course_add(request):
    """
    Redirects to the course edit page to add a new course. This is a placeholder for future expansion or refactoring.

    :param request: HttpRequest object.
    :return: HttpResponse object rendering the course edit template.
    """
    return render(request, 'administrator/course_edit.html')
