from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse

from lecturer.models import Course, LecturerCourseAssignment, Lecturer


# Admin - Course Management
# This method is to show the course management page
# @return: courses a list of courses
def course_management(request):
    # courses = Course.objects.all()
    # course with lectrer name, and count of feedbacks
    courses = Course.objects.all().values('courseId', 'courseName', 'programType', 'semester', 'lecturercourseassignment__lecturerId__lecturerName').order_by('courseId')
    return render(request, 'administrator/course_management.html', {'courses': courses})


# Admin - Course Edit Page
# This page is for the admin to edit the course details
# @param course_id: the id of the course
# @return: course
def course_edit(request):
    # print(request)
    course_id = request.GET.get('course_id')
    # get all
    course = get_object_or_404(Course, courseId=course_id)
    # .values('courseId', 'courseName', 'programType', 'semester', 'lecturercourseassignment__lecturerId__lecturerName')
    lecturer_name = course.lecturercourseassignment_set.all().values('lecturerId__lecturerName').first()
    course = {'courseId': course.courseId, 'courseName': course.courseName, 'programType': course.programType, 'semester': course.semester, 'lecturerName': lecturer_name}

    # print("course_detail is here: ")
    # print(course)
    return render(request, 'administrator/create_course_management.html', {'course': course})



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
        lecturer_name = request.POST.get('lecturer_name')
        # TODO: convert program type
        semester = request.POST.get('semester')
        course = Course(courseId=course_id, courseName=course_name, programType=program_type, semester=semester)
        course.save()

        # find lecturer id by lecturer name
        lecturer = Lecturer.get_object_or_404(Lecturer, lecturerName=lecturer_name)
        # right now, one course can only have one lecturer
        # if the course already has a lecturer, update the lecturer
        if course.lecturercourseassignment_set.exists():
            course.lecturercourseassignment_set.update(lecturerId=lecturer.lecturerId)
        else:
            # if the course does not have a lecturer, create a new lecturer
            lecturer_course_assignment = LecturerCourseAssignment(lecturerId=lecturer.lecturerId, courseId=course)
            lecturer_course_assignment.save()

        # or redirect to the course management page
        return render(request, reverse('administrator:course_management'), {'success': True})



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
#     return render(request, 'administrator/create_course_management.html')