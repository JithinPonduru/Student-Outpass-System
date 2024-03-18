from django.db import models
from django.utils import timezone
import pytz

indian_timezone = pytz.timezone('Asia/Kolkata')

class Student(models.Model):
    roll = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    otp = models.IntegerField(null=True, blank=True)
    uid = models.IntegerField(null=True, blank=True)
    validation = models.BooleanField(default=False)
    StudentOut = models.BooleanField(default=False)
    StudentIn = models.BooleanField(default=True)
    OutTime = models.CharField(max_length=200)
    InTime = models.CharField(max_length=200)
    otp_expiry = timezone.now().astimezone(indian_timezone) + timezone.timedelta(minutes=5)

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
    out_time = models.DateTimeField()
    in_time = models.DateTimeField(null=True, blank=True)
    now = timezone.now().astimezone(indian_timezone)
    TodayDate = now.strftime("%A, %d %B %Y %H:%M:%S")

    def __str__(self):
        return f"{self.student.roll}"
