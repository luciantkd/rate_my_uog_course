from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse
from django.urls import reverse

from administrator.models import Admin
from lecturer.models import Course, Lecturer
from student.models import CourseFeedback
from rateMyUogCourse.models import WebsiteFeedback, CourseSearchTable


# View for testing viewing the Feedback Management page
# def feedback_management(request):
#     return render(request, 'administrator/feedback_management.html')

# View for testing viewing the Reported Reviews Management page
# def reported_reviews_management(request):
#     return render(request, 'administrator/reported_reviews_management.html')

# View for testing viewing the Lecturer Management page
def lecturer_management(request):
    # get lecturer list except passwords
    lecturers = Lecturer.objects.all().values('lecturerId', 'lecturerName', 'designation', 'email').order_by('lecturerId')
    print(lecturers)
    return render(request, 'administrator/lecturer_management.html', {'lecturers': lecturers})


def lecturer_edit(request):
    # get lecturer id from request
    lecturer_id = request.GET.get('lecturer_id')
    print(lecturer_id)
    # get lecturer entity
    lecturer_entity = (get_object_or_404(Lecturer, pk=lecturer_id))
    # values('lecturerId', 'lecturerName', 'designation'))
    lecturer_entity = {'lecturerId': lecturer_entity.lecturerId, 'lecturerName': lecturer_entity.lecturerName,
                       'designation': lecturer_entity.designation, 'email': lecturer_entity.email}
    print(lecturer_entity)
    return render(request, 'administrator/lecturer_edit.html', {'lecturer_entity': lecturer_entity})

def lecturer_save_post(request):
    if request.method == 'POST':
        # 获取表单数据
        lecturer_id = request.POST.get('lecturerId')
        lecturer_name = request.POST.get('lecturerName')
        designation = request.POST.get('designation')
        email = request.POST.get('Email')
        password = request.POST.get('Password')

        # 根据ID获取讲师对象
        lecturer = get_object_or_404(Lecturer, pk=lecturer_id)

        # 更新讲师信息
        lecturer.lecturerName = lecturer_name
        lecturer.designation = designation
        lecturer.email = email

        # 如果密码字段不为空，则更新密码
        if password:
            # TODO: Hash the password
            lecturer.password = password

        # 保存更改到数据库
        lecturer.save()

        # 重定向到讲师列表或其他页面
        return redirect(reverse('administrator:lecturer_management'))
    else:
        # 如果不是POST请求，则重定向到编辑页面或显示错误
        return redirect(reverse('administrator:lecturer_management'))