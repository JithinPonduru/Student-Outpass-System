from django.http import HttpResponse
from django.shortcuts import render, redirect
from IDPAPP.models import OutRecord, Student, Test
import random
from twilio.rest import Client
from IDPAPP import Twiliodetails
from django.utils import timezone
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt


indian_timezone = timezone.get_fixed_timezone(330) 


@csrf_exempt
def index(request):
    if request.method == 'POST':
        try:  
            received_data = json.loads(request.body)
            Name = received_data.get('name')
            roll_number = received_data.get('roll')
            roll_number = roll_number[:13]
            Uid = received_data.get('uid')
            General = received_data.get('General')
            Home = received_data.get('Home')
        except json.JSONDecodeError:
            Name = request.POST.get('name')
            roll_number = request.POST.get('roll')
            roll_number = roll_number[:13]
            Uid = request.POST.get('uid')
            General = request.POST.get('General')
            Home = request.POST.get('Home')
        try:
            student = Test.objects.get(roll=roll_number)
            phone_number = Test.objects.get(roll=roll_number).phone

            OTP = random.randint(100000, 999999)
            account_sid = Twiliodetails.account_sid
            auth_token = Twiliodetails.auth_token
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f'\nHello, {OTP} is your OTP. Your child is leaving the camp with admission number {roll_number} Name {student.name}. If you consent to your child leaving the campus, please share this. Good for a duration of five minutes.',
                from_='+18587790079',
                to='+91' + str(phone_number)
            )
            try:
                student = Student.objects.get(roll=roll_number)
                student.otp = OTP
                student.GeneralOuting = General
                student.HomeOuting = Home
            except Student.DoesNotExist:
                student = Student.objects.create(roll=roll_number, name=Name, uid=Uid, otp=OTP,otp_expiry=timezone.now().astimezone(indian_timezone) + timezone.timedelta(minutes=5))
            student.validation = False
            student.InTime = ""
            student.OutTime = ""
            student.GeneralOuting = General
            student.HomeOuting = Home
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
                student.validation = True
                student.showinnotverified = False
                student.save()
                return render(request,'index.html' ,{'verification' : 'OTP Verified'})      
            
            elif not student.validation:
                return render(request,'index.html' ,{'verification' : 'OTP Not Verified. Incorrect OTP'}) 
            
            else:
                return render(request,'index.html' ,{'verification' : 'Invalid OTP. Please try again.'}) 
        
        except Student.DoesNotExist:
            return HttpResponse("Student not found.")
    else:
        return HttpResponse("Invalid request method.")

@csrf_exempt
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
            student = Student.objects.get(roll=roll_number, validation=True,StudentOut=False)
            now = timezone.now().astimezone(indian_timezone)
            timevar = now.strftime("%A, %d %B %Y %H:%M:%S")
            student.OutTime = timevar
            student.StudentOut = True
            student.StudentIn = False
            student.InTime = "Still out of campus"
            phone_number = Test.objects.get(roll=roll_number).phone
            account_sid = Twiliodetails.account_sid
            auth_token = Twiliodetails.auth_token
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f'\nYour child with admission number {roll_number} has left the campus. If you have not consented to this, please contact the authorities.',
                from_='+18587790079',
                to='+91' + str(phone_number)
            )
            student.save()
            dataitem = OutRecord.objects.create(student=student, OutDate=timevar , GeneralOuting=student.GeneralOuting, HomeOuting=student.HomeOuting)
            dataitem.save()
            return render(request, 'OutGoing.html', {'roll_number': roll_number})
        except Student.DoesNotExist:
            return HttpResponse("Student not validated or not found or already marked as out of campus.")
    else:
        return render(request, 'OutGoing.html')
    
@csrf_exempt
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
            student = Student.objects.get(roll=roll_number, validation=True,StudentOut=True)
            now = timezone.now().astimezone(indian_timezone)
            hrs = now.hour
            timevar = now.strftime("%A, %d %B %Y %H:%M:%S")
            if hrs >= 21:
                student.lateentryflag = True
            student.validation = False
            student.StudentOut = False
            student.StudentIn = True
            student.InTime = timevar
            account_sid = Twiliodetails.account_sid
            auth_token = Twiliodetails.auth_token
            client = Client(account_sid, auth_token)
            phone_number = Test.objects.get(roll=roll_number).phone
            message = client.messages.create(
                body=f'\nYour child with admission number {roll_number} has returned to the campus. If you have not consented to this, please contact the authorities.',
                from_='+18587790079',
                to='+91' + str(phone_number)
            )


            try:
                dataitem = OutRecord.objects.get(student=student, InDate="")
                dataitem.InDate = timevar
                dataitem.lateenteryflag = student.lateentryflag
                dataitem.save()
            except OutRecord.DoesNotExist:
                return HttpResponse ("OutRecord not found.")
            student.save()
            return render(request, 'Incoming.html', {'roll_number': roll_number})
        except Student.DoesNotExist:
            return HttpResponse("Student not validated or not found or already marked as in campus.")
    else:
        return render(request, 'Incoming.html')

@csrf_exempt
def functiontemp(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            roll_number = received_data.get('roll')
        except json.JSONDecodeError:
            roll_number = request.POST.get('roll')

        roll_number = roll_number[:13]  # Truncate to 13 characters if longer

        try:
            student = Student.objects.get(roll=roll_number)
            out_records = OutRecord.objects.filter(student=student)
            return render(request, 'StudentRecords.html', {'students': out_records,'studentdetails' : student})
        except Student.DoesNotExist:
            return HttpResponse("Student not found.")
    else:
        return render(request, 'StudentRecords.html')
    
@csrf_exempt
def ResendOTP(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            roll_number = received_data.get('roll')
            roll_number = roll_number[:13]
        except json.JSONDecodeError:
            roll_number = request.POST.get('roll')
            roll_number = roll_number[:13]
        try:
            student = Student.objects.get(roll=roll_number)
            phone_number = Test.objects.get(roll=roll_number).phone
            if student.otp_expiry < timezone.now():
                OTP = random.randint(100000, 999999)
                student.otp = OTP
                student.otp_expiry = timezone.now().astimezone(indian_timezone) + timezone.timedelta(minutes=5)
                student.save()
                account_sid = Twiliodetails.account_sid
                auth_token = Twiliodetails.auth_token
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    body=f'\nHello, {OTP} is your OTP. Your child is leaving the camp with admission number {roll_number} Name {student.name}. If you consent to your child leaving the campus, please share this. Good for a duration of five minutes.',
                    from_='+18587790079',
                    to='+91' + str(phone_number)
                )
                return render(request, 'index.html', {'resendstatus':"OTP sent successfully."})
            else:
                return render(request, 'index.html', {'resendstatus':"OTP Not Expired"})
                
        except Student.DoesNotExist:
            return  render(request, 'index.html', {'resendstatus': "Student not found."})
    else:
        return render(request, 'index.html')
    

@csrf_exempt
def ViewOTP(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            roll_number = received_data.get('roll')
            roll_number = roll_number[:13]
        except json.JSONDecodeError:
            roll_number = request.POST.get('roll')
            roll_number = roll_number[:13]
        try:
            student = Student.objects.get(roll=roll_number)
            if student.otp_expiry < timezone.now():
                return HttpResponse('OTP expired. Please request a new OTP.')
            else:
                context = {
                    'temp': {
                        'validation': True,  # Example boolean value for validation
                        'viewotp': student.otp,  # Example value for viewotp
                        'roll_number': student.roll  # Example value for roll_number
                    }
                }
                return render(request, 'index.html', context)
        except Student.DoesNotExist:
            return HttpResponse("Student not found.")
    else:
        return render(request, 'index.html')
    



def ListofApplicants(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            roll_number = received_data.get('roll')
        except json.JSONDecodeError:
            roll_number = request.POST.get('roll')
        try:
            Notvalidatedstudents = Student.objects.filter(roll=roll_number,showinnotverified=True)
            return render(request, 'ListofApplicants.html', {'Notvalidatedstudents': Notvalidatedstudents})
        except Student.DoesNotExist:
            return HttpResponse("Student not found.")
    else:
        Notvalidatedstudents = Student.objects.filter(validation=False,showinnotverified=True)
        return render(request, 'ListofApplicants.html', {'Notvalidatedstudents': Notvalidatedstudents})