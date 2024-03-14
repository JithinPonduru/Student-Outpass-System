from django.http import HttpResponse
from django.shortcuts import redirect, render
from IDPAPP.models import Student, Test
import random
from twilio.rest import Client
from IDPAPP import Twiliodetails
from django.utils import timezone
import pytz
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            Name = received_data.get('name')
            roll_number = received_data.get('roll')
        except json.JSONDecodeError:
            Name = request.POST.get('name')
            roll_number = request.POST.get('roll')
        print(Name)
        print(roll_number)
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
            account_sid = Twiliodetails.account_sid
            auth_token = Twiliodetails.auth_token
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f'Hi, this is your OTP: {otp}. Valid for 5 minutes.',
                from_='+18587790079',
                to='+91' + str(phone_number)
            )
            try:
                student = Student.objects.get(roll=roll_number)
            except Student.DoesNotExist:
                student = Student.objects.create(roll=roll_number, name=Name)
            return render(request, 'index.html')
        except Test.DoesNotExist:
            return HttpResponse(f"No student found with roll number {roll_number}")

    return render(request, 'index.html')


@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        if not stored_otp:
            return HttpResponse("OTP expired. Please request a new OTP.")
        if otp_input == str(stored_otp):
            # OTP is verified, do something
            roll_number = request.session.get('roll_number')
            Name = request.session.get('Name')
            validation = True
            request.session['validation'] = validation
            del request.session['otp']
            try:
                student = Student.objects.get(roll=roll_number)
                student.validation = validation
                student.save()
            except Student.DoesNotExist:
                return HttpResponse("Student not found.")
            return render(request, 'OutGoing.html')
        else:
            del request.session['otp']
            return HttpResponse("Invalid OTP")

    return HttpResponse("Use the form to submit a POST request with the OTP.")

def OutGoing(request):
    if request.session.get('validation'):
        roll_number = request.session.get('roll_number')
        try:
            student = Student.objects.get(roll=roll_number)
            indian_timezone = pytz.timezone('Asia/Kolkata')
            now = timezone.now().astimezone(indian_timezone)
            student.OutTime = now.strftime("%A, %d %B %Y %H:%M:%S")
            student.StudentOut = True
            student.StudentIn = False
            student.InTime = "Still out of campus"
            student.save()
            return render(request, 'Incoming.html', {'roll_number': roll_number})
        except Student.DoesNotExist:
            return HttpResponse("Student not found.")
    return HttpResponse("Student not validated.")



def Incoming(request):
    if request.session.get('validation'):
        roll_number = request.session.get('roll_number')
        try:
            student = Student.objects.get(roll=roll_number)
            indian_timezone = pytz.timezone('Asia/Kolkata')
            now = timezone.now().astimezone(indian_timezone)
            student.StudentIn = True
            student.StudentOut = False
            student.InTime = now.strftime("%A, %d %B %Y %H:%M:%S")
            student.save()
            return redirect('/')
        except Student.DoesNotExist:
            return HttpResponse("Student not found.")
    return HttpResponse("Student not validated.")
