from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse

from lecturer.models import Course, LecturerCourseAssignment, Lecturer


def course_management(request):
    '''
    This method is to show the course management page
    :param request:
    :return: ourses a list of courses
    '''
    # courses = Course.objects.all().values('courseId', 'courseName', 'programType', 'semester', 'lecturercourseassignment__lecturerId__lecturerName').order_by('courseId')
    courses_list = Course.objects.all().order_by('courseId')
    courses = []

    for course in courses_list:
        lecturer_names = course.lecturercourseassignment_set.all().values_list('lecturerId__lecturerName', flat=True)
        lecturer_names_str = ', '.join(lecturer_names)

        courses.append({
            'courseId': course.courseId,
            'courseName': course.courseName,
            'programType': course.programType,
            'semester': course.semester,
            'lecturercourseassignment__lecturerId__lecturerName': lecturer_names_str
        })
    return render(request, 'administrator/course_management.html', {'courses': courses})


# Admin - Course Edit Page
def course_edit(request):
    '''
    This page is for the admin to edit the course details
    :param request: the course_id of the course
    :return: course
    '''
    # print(request)
    course_id = request.GET.get('course_id')
    # get all
    course = get_object_or_404(Course, courseId=course_id)
    # .values('courseId', 'courseName', 'programType', 'semester', 'lecturercourseassignment__lecturerId__lecturerName')
    # this is a sets of lecturer
    lecturer_names = course.lecturercourseassignment_set.all().values_list('lecturerId__lecturerName', flat=True)
    lecturer_names_str = ', '.join(lecturer_names)
    course = {'courseId': course.courseId, 'courseName': course.courseName, 'programType': course.programType, 'semester': course.semester, 'lecturerName': lecturer_names_str}

    # print("course_detail is here: ")
    # print(course)
    return render(request, 'administrator/course_edit.html', {'course': course})



# Admin - Course Edit Post
# This method is to update or create a course, using post method
# @param request: the request
# @param course: an entity of course
# @return: boolean success
def course_edit_post(request):
    if (request.method == 'POST'):
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course_name')
        program_type = request.POST.get('program_type')
        lecturer_names = request.POST.get('professor').split(',')  # 假设讲师名字是逗号分隔的
        print(course_name)
        # TODO: convert program type
        semester = request.POST.get('semester')
        semester = 2023
        # 更新或创建课程
        course, created = Course.objects.update_or_create(
            courseId=course_id,
            defaults={'courseName': course_name, 'programType': program_type, 'semester': semester}
        )

        for lecturer_name in lecturer_names:
            lecturer_name = lecturer_name.strip()
            lecturer, _ = Lecturer.objects.get_or_create(lecturerName=lecturer_name)
            LecturerCourseAssignment.objects.update_or_create(lecturerId=lecturer, courseId=course)

        # or redirect to the course management page
        return redirect(reverse('administrator:course_management'))



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
    return render(request, 'administrator/course_add.html')
def course_add_post(request):
    if request.method == "POST":
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course_name')
        program_type = request.POST.get('program_type')
        semester = request.POST.get('semester')
        lecturer_name = request.POST.get('lecturer_name')
        # TODO: WE DO NOT HAVE SEMESTER
        if semester is None:
            semester = 2023/2024
        course = Course(courseId=course_id, courseName=course_name, programType=program_type, semester=semester)
        course.save()
        if lecturer_name is not None:
            lecturer = Lecturer.get_object_or_404(Lecturer, lecturerName=lecturer_name)
            lecturer_course_assignment = LecturerCourseAssignment(lecturerId=lecturer.lecturerId, courseId=course)
            lecturer_course_assignment.save()
        return redirect(reverse('administrator:course_management'))