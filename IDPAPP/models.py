from django.db import models
from django.utils import timezone
import pytz

indian_timezone = timezone.get_fixed_timezone(330) 

class Student(models.Model):
    roll = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    otp = models.IntegerField(null=True, blank=True)
    uid = models.IntegerField(null=True, blank=True)
    validation = models.BooleanField(default=False)
    StudentOut = models.BooleanField(default=False)
    StudentIn = models.BooleanField(default=True)
    HomeOuting = models.BooleanField(default=False)
    GeneralOuting = models.BooleanField(default=True)
    OutTime = models.CharField(max_length=200)
    InTime = models.CharField(max_length=200)
    otp_expiry = models.DateTimeField()
    showinnotverified = models.BooleanField(default=True)
   
    def __str__(self):
        return self.roll


class Test(models.Model):
    roll = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.roll

class OutRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='out_records')
    OutDate = models.CharField(max_length=200)
    InDate = models.CharField(max_length=200)
    HomeOuting = models.BooleanField(default=False)
    GeneralOuting = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.student.roll}"
