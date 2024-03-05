from django.db import models

# Create your models here.

class Admin(models.Model):
    userName = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=8)
    
    def __str__(self):
        return self.userName