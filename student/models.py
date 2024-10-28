from django.db import models

from lecturer.models import Course


#Table for storing student data
class Student(models.Model):
    guid = models.CharField(max_length=7, unique=True, primary_key=True)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    password = models.TextField()
    programType = models.CharField(max_length=4)

    def __str__(self):
        return self.guid

# Table for storing detailed course feedback
class CourseFeedback(models.Model):
    feedbackId = models.AutoField(unique=True, primary_key=True)
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    guid = models.ForeignKey(Student, on_delete=models.CASCADE)
    overall = models.IntegerField()
    difficulty = models.IntegerField()
    usefulness = models.IntegerField()
    workload = models.IntegerField()
    examFormat = models.CharField(max_length=50)
    evaluationMethod = models.CharField(max_length=250)
    lecturerRating = models.IntegerField()
    gradeReceived = models.CharField(max_length=2)
    recommendCourse = models.BooleanField()
    textFeedback = models.TextField()
    likes = models.IntegerField(default=0)
    reported = models.IntegerField(default=0)
    approved = models.BooleanField(default=True)
    feedbackDateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.feedbackId

# Table for Student Feedback Like relationship
class StudentFeedbackLikes(models.Model):
    guid = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedbackId = models.ForeignKey(CourseFeedback, on_delete=models.CASCADE)
