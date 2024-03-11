from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse
from django.contrib import messages
from lecturer.models import Course, LecturerCourseAssignment, Lecturer
from rateMyUogCourse.models import CourseSearchTable


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
    if request.method == 'POST':
        course_id = request.POST.get('course_id', '').strip()
        course_name = request.POST.get('course_name', '').strip()
        program_type = request.POST.get('program_type', '').strip()
        lecturer_names = [name.strip() for name in request.POST.get('professor', '').split(',')]
        semester = request.POST.get('semester', '2023').strip()

        # 示例错误判定：检查课程名称是否为空
        if not course_name:
            messages.error(request, 'Course name cannot be empty.')
            return redirect(reverse('administrator:course_edit'))

        # 仅在所有验证通过后更新或创建课程
        course, created = Course.objects.update_or_create(
            courseId=course_id,
            defaults={'courseName': course_name, 'programType': program_type, 'semester': semester}
        )

        # 处理讲师名字
        for lecturer_name in lecturer_names:
            try:
                lecturer = Lecturer.objects.get(lecturerName=lecturer_name)
                LecturerCourseAssignment.objects.update_or_create(lecturerId=lecturer, courseId=course)
            except Lecturer.DoesNotExist:
                # 如果找不到讲师，向用户显示错误消息
                messages.error(request, f'Lecturer "{lecturer_name}" not found. Please check the name and try again.')
                # 返回到编辑页面，附带之前输入的信息，以便用户可以更正
                return render(request, 'administrator/course_edit.html', {
                    'course': {
                        'courseId': course_id,
                        'courseName': course_name,
                        'programType': program_type,
                        'semester': semester,
                        'lecturerName': ', '.join(lecturer_names)
                    }
                })

        return redirect(reverse('administrator:course_management'))

    # 如果请求方法不是POST，重定向到某个视图
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
            semester = 2023
        course = Course(courseId=course_id, courseName=course_name, programType=program_type, semester=semester)
        course.save()
        if lecturer_name is not None:
            lecturer = Lecturer.get_object_or_404(Lecturer, lecturerName=lecturer_name)
            lecturer_course_assignment = LecturerCourseAssignment(lecturerId=lecturer.lecturerId, courseId=course)
            lecturer_course_assignment.save()
        # create search table for the course
        course_search = CourseSearchTable(courseId=course, courseName=course_name)
        course_search.save()
        return redirect(reverse('administrator:course_management'))