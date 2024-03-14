from django.db import models


# Lecturer Model
class Lecturer(models.Model):
    lecturerId = models.CharField(max_length=20, unique=True, primary_key=True)
    lecturerName = models.CharField(max_length=200)
    designation = models.CharField(max_length=250)
    email = models.CharField(max_length=100)
    password = models.TextField()

    def __str__(self):
        return self.lecturerId

# Course Model
class Course(models.Model):
    courseId = models.CharField(max_length=20, unique=True, primary_key=True)
    courseName = models.CharField(max_length=200)
    programType = models.CharField(max_length=4)
    semester = models.IntegerField()

    def __str__(self):
        return self.courseName

# Course and lecturer relationship table
class LecturerCourseAssignment(models.Model):
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturerId = models.ForeignKey(Lecturer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.courseId) + str(self.lecturerId)
