from django.http import HttpResponse
from django.shortcuts import render
from IDPAPP.models import Test
import random
from twilio.rest import Client
from IDPAPP import Twiliodetails

def index(request):
    if request.method == 'POST':
        roll_number = request.POST.get('roll')
        try:
            student = Test.objects.get(roll=roll_number)
            phone_number = student.phone

            # Generate OTP and store it in session
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            
            # Send OTP via Twilio
            account_sid = Twiliodetails.account_sid
            auth_token = Twiliodetails.auth_token
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=f'Hi, this is your OTP: {otp}. Valid for 5 minutes.',
                from_='+18587790079',
                to='+91' + str(phone_number)
            )

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
            return HttpResponse("OTP is verified")
        else:
            return HttpResponse("Invalid OTP")

    return HttpResponse("Use the form to submit a POST request with the OTP.")

def about(request):
    roll_number = 'AP21110010890'
    try:
        student = Test.objects.get(roll=roll_number)
        phone_number = student.phone
        return HttpResponse(f"Phone number of roll {roll_number} is {phone_number}")
    except Test.DoesNotExist:
        return HttpResponse(f"No student found with roll number {roll_number}")
