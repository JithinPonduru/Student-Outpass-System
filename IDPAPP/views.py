from django.http import HttpResponse
from django.shortcuts import render, redirect
from IDPAPP.models import Student, Test
import random
from twilio.rest import Client
from IDPAPP import Twiliodetails
from django.utils import timezone
import pytz
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

indian_timezone = pytz.timezone('Asia/Kolkata')

@csrf_exempt
def index(request):
    print(str(timezone.now().astimezone(indian_timezone) + timezone.timedelta(minutes=5)))
    if request.method == 'POST':
        try:
            # 1548100121    
            received_data = json.loads(request.body)
            Name = received_data.get('name')
            roll_number = received_data.get('roll')
            roll_number = roll_number[:13]
            Uid = received_data.get('uid')
        except json.JSONDecodeError:
            Name = request.POST.get('name')
            roll_number = request.POST.get('roll')
            roll_number = roll_number[:13]
            Uid = request.POST.get('uid')
        print(Name, roll_number, Uid)
        try:
            student = Test.objects.get(roll=roll_number)
            phone_number = student.phone

            OTP = random.randint(100000, 999999)
            # account_sid = Twiliodetails.account_sid
            # auth_token = Twiliodetails.auth_token
            # client = Client(account_sid, auth_token)
            # message = client.messages.create(
            #     body=f'\nHello, {OTP} is your OTP. Your child is leaving the camp with admission number {roll_number}. If you consent to your child leaving the campus, please share this. Good for a duration of five minutes.',
            #     from_='+18587790079',
            #     to='+91' + str(phone_number)
            # )
            print(OTP)

            try:
                student = Student.objects.get(roll=roll_number)
                student.otp = OTP
                
            except Student.DoesNotExist:
                student = Student.objects.create(roll=roll_number, name=Name, uid=Uid, otp=OTP,otp_expiry=timezone.now().astimezone(indian_timezone) + timezone.timedelta(minutes=5))
            student.validation = False
            student.InTime = ""
            student.OutTime = ""
            student.otp_expiry = timezone.now().astimezone(indian_timezone) + timezone.timedelta(minutes=5) + timezone.timedelta(hours=5, minutes=30)
            student.save()
            return render(request, 'index.html')
        except Test.DoesNotExist:
            return HttpResponse(f"No student found with roll number {roll_number}")

    return render(request, 'index.html')

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            roll_number = received_data.get('roll')
            roll_number = roll_number[:13]
            otp_input = received_data.get('otp')
        except json.JSONDecodeError:
            roll_number = request.POST.get('roll')
            roll_number = roll_number[:13]
            otp_input = request.POST.get('otp')
        try:
            student = Student.objects.get(roll=roll_number)
            if student.otp_expiry < timezone.now():
                return HttpResponse('OTP expired. Please request a new OTP.')
            
            elif str(otp_input) == str(student.otp):
                print('OTP verified')
                student.validation = True
                student.save()
                print(student.validation)
                return redirect('/' ,{'verification' : True})      
            
            elif not student.validation:
                return HttpResponse(f'Student is not Verified with Roll_number : {student.roll} and Name : {student.name} Please request an OTP.')
            
            else:
                return HttpResponse("Invalid OTP. Please try again.")
        
        except Student.DoesNotExist:
            return HttpResponse("Student not found.")
    else:
        return HttpResponse("Invalid request method.")


def OutGoing(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            roll_number = received_data.get('roll')
            roll_number = roll_number[:13]
        except json.JSONDecodeError:
            roll_number = request.POST.get('roll')
            roll_number = roll_number[:13]

        try:
            print(roll_number)
            student = Student.objects.get(roll=roll_number, validation=True)
            print('student validated')
            now = timezone.now().astimezone(indian_timezone)
            student.OutTime = now.strftime("%A, %d %B %Y %H:%M:%S")
            student.StudentOut = True
            student.StudentIn = False
            student.InTime = "Still out of campus"
            student.save()
            return render(request, 'Incoming.html', {'roll_number': roll_number})
        except Student.DoesNotExist:
            return HttpResponse("Student not validated or not found.")
    else:
        return render(request, 'OutGoing.html')

def Incoming(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            roll_number = received_data.get('roll')
            roll_number = roll_number[:13]
        except json.JSONDecodeError:
            roll_number = request.POST.get('roll')
            roll_number = roll_number[:13]

        try:
            print(roll_number)
            student = Student.objects.get(roll=roll_number, validation=True)
            print('student validated')
            now = timezone.now().astimezone(indian_timezone)
            student.validation = False
            student.StudentOut = False
            student.StudentIn = True
            student.InTime = now.strftime("%A, %d %B %Y %H:%M:%S")
            student.save()
            return render(request, 'Incoming.html', {'roll_number': roll_number})
        except Student.DoesNotExist:
            return HttpResponse("It was found that the student was suspicious of leaving without permission.")
    else:
        return render(request, 'Incoming.html')
