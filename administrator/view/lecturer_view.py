from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse

from lecturer.models import Lecturer
from rateMyUogCourse.views import encryptPassword
from django.contrib import messages


def lecturer_management(request):
    search_query = request.GET.get('query', '')

    # 使用 Q 对象进行复杂查询，允许同时按名字和电子邮件搜索
    if search_query:
        lecturers = Lecturer.objects.filter(
            Q(lecturerName__icontains=search_query) |
            Q(email__icontains=search_query)
        ).values('lecturerId', 'lecturerName', 'designation', 'email').order_by('lecturerId')
    else:
        lecturers = Lecturer.objects.all().values('lecturerId', 'lecturerName', 'designation', 'email').order_by('lecturerId')

    return render(request, 'administrator/lecturer_management.html', {'lecturers': lecturers})


def lecturer_edit(request):
    lecturer_id = request.GET.get('lecturer_id')
    if request.method == 'POST':
        # 获取表单数据
        lecturer_id = request.POST.get('lecturerId', '').strip()
        lecturer_name = request.POST.get('lecturerName', '').strip()
        designation = request.POST.get('designation', '').strip()
        email = request.POST.get('Email', '').strip()
        password = request.POST.get('Password', '').strip()

        # 输入验证
        if not all([lecturer_name, designation, email]):
            messages.error(request, "Name, designation, and email cannot be empty.")
            return render(request, 'administrator/lecturer_edit.html', {
                'lecturer_entity': {
                    'lecturerId': lecturer_id,
                    'lecturerName': lecturer_name,
                    'designation': designation,
                    'email': email,
                }
            })

        if lecturer_id:  # 编辑现有讲师
            lecturer = get_object_or_404(Lecturer, pk=lecturer_id)
        else:  # 添加新讲师
            # if password is not provided, return error message
            if not password:
                messages.error(request, "Password cannot be empty.")
                return render(request, 'administrator/lecturer_edit.html', {
                    'lecturer_entity': {
                        'lecturerId': lecturer_id,
                        'lecturerName': lecturer_name,
                        'designation': designation,
                        'email': email,
                    }
                })
            lecturer_id = email.split('@')[0]  # 或其他生成讲师ID的逻辑
            lecturer = Lecturer(lecturerId=lecturer_id)

        lecturer.lecturerName = lecturer_name
        lecturer.designation = designation
        lecturer.email = email

        if password:  # 如果提供了密码，则更新密码
            lecturer.password = encryptPassword(password)

        lecturer.save()
        return redirect(reverse('administrator:lecturer_management'))

    else:  # GET请求
        lecturer_entity = {}
        if lecturer_id:  # 编辑模式
            lecturer = get_object_or_404(Lecturer, pk=lecturer_id)
            lecturer_entity = {
                'lecturerId': lecturer.lecturerId,
                'lecturerName': lecturer.lecturerName,
                'designation': lecturer.designation,
                'email': lecturer.email
            }
        return render(request, 'administrator/lecturer_edit.html',
                      {'lecturer_entity': lecturer_entity})


def lecturer_delete(request):
    # django delete post
    if request.method == "POST":
        lecturer_id = request.POST.get('lecturer_id')
        lecturer = get_object_or_404(Lecturer, pk=lecturer_id)
        lecturer.delete()
        return redirect(reverse('administrator:lecturer_management'))  # Redirect to the lecturer management page
    else:
        return redirect(reverse('administrator:lecturer_management'))
