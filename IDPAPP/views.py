import time
from django.http import HttpResponse
from django.shortcuts import render
from IDPAPP.models import Student, Test
import random
from twilio.rest import Client
from IDPAPP import Twiliodetails

def index(request):
    if request.method == 'POST':
        Name = request.POST.get('name')
        roll_number = request.POST.get('roll')
        try:
            student = Test.objects.get(roll=roll_number)
            phone_number = student.phone

            # Generate OTP and store it in session
            otp = random.randint(100000, 999999)
            print(otp)
            request.session['otp'] = otp
            request.session['Name'] = Name
            request.session['roll_number'] = roll_number
            request.session.set_expiry(300)  # Set expiry time for the session to 5 minutes
            # Send OTP via Twilio
            # account_sid = Twiliodetails.account_sid
            # auth_token = Twiliodetails.auth_token
            # client = Client(account_sid, auth_token)
            # message = client.messages.create(
            #     body=f'Hi, this is your OTP: {otp}. Valid for 5 minutes.',
            #     from_='+18587790079',
            #     to='+91' + str(phone_number)
            # )

            return render(request, 'index.html')
        except Test.DoesNotExist:
            return HttpResponse(f"No student found with roll number {roll_number}")

    return render(request, 'index.html')

def verify_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        if not stored_otp:
            return HttpResponse("OTP expired. Please request a new OTP.")
        if otp_input == str(stored_otp):
            # OTP is verified, do something
            validation = True
            request.session['validation'] = validation
            return render(request, 'verified.html')
        else:
            return HttpResponse("Invalid OTP")

    return HttpResponse("Use the form to submit a POST request with the OTP.")

def verified(request):
    if request.session.get('validation'):
        roll_number = request.session.get('roll_number')
        Name = request.session.get('Name')
        validation = request.session.get('validation')
        StudentOut = True
        StudentIn = False
        InTime = ""
        OutTime = ""
        if StudentOut:
            InTime = time.strftime("%Y-%m-%d %H:%M:%S")
        elif StudentIn:
            OutTime = time.strftime("%Y-%m-%d %H:%M:%S")
            InTime = 'Not yet entered to College.'
        if StudentOut:
            student = Student.objects.create(roll=roll_number, name=Name, validation=validation, StudentOut=StudentOut, StudentIn=StudentIn, OutTime=OutTime,InTime=InTime)
            return render(request, 'verified.html')
        elif StudentIn:
            # Update the existing student record
            student = Student.objects.get(roll=roll_number)
            StudentIn = True
            student.StudentIn = StudentIn
            student.InTime = InTime
            student.save()
            return HttpResponse("Student not validated.")
    return HttpResponse("Student not validated.")
