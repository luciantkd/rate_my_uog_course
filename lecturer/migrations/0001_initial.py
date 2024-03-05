# Generated by Django 2.1.5 on 2024-03-05 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('courseId', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('courseName', models.CharField(max_length=200)),
                ('programType', models.CharField(max_length=4)),
                ('semester', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('lecturerId', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('lecturerName', models.CharField(max_length=200)),
                ('designation', models.CharField(max_length=250)),
                ('password', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LecturerCourseAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecturer.Course')),
                ('lecturerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecturer.Lecturer')),
            ],
        ),
    ]
