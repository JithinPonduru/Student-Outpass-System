# models.py
from django.db import models

class Student(models.Model):
    roll = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)

    validation = models.BooleanField(default=False)

    StudentOut = models.BooleanField(default=False)
    StudentIn = models.BooleanField(default=True)
    
    OutTime = models.DateTimeField(auto_now=True)
    InTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.roll

class Test(models.Model):
    roll = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.roll
