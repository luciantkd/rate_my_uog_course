from django.db import models
from lecturer.models import Course
# Create your models here.

class CourseSearchTable(models.Model):
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
    courseName = models.CharField(max_length=200)
    overall = models.IntegerField()
    difficulty = models.IntegerField()
    usefulness = models.IntegerField()
    workload = models.IntegerField()
    reviews = models.IntegerField()
    wouldRecommend = models.FloatField()
    professorRating = models.IntegerField()

    def __str__(self):
        return str(self.courseId)
    

class WebsiteFeedback(models.Model):
    # # feedbackId auto increment
    feedbackId = models.AutoField(primary_key = True, unique = True)
    feedbackTime = models.DateTimeField(auto_now_add = True)
    friendly = models.IntegerField()
    overall = models.IntegerField()
    aesthetic = models.IntegerField()
    comment = models.TextField(blank=True)
    
    def __str__(self):
        return str(self.feedbackId)