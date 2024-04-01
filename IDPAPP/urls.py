"""IDPSERVER URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from IDPAPP import views

admin.site.site_header = "IDP Admin"
admin.site.site_title = "IDP Admin Portal"
admin.site.index_title = "Welcome to IDP Researcher Portal"

urlpatterns = [
    path('',views.index,name='index'),
    path('otp',views.verify_otp,name='OTP'),
    path('OutGoing',views.OutGoing,name='OutGoing'),
    path('InComing',views.Incoming,name='Incoming'),
    path('StudentRecord',views.functiontemp,name='studentrecord'),
    path('resendotp',views.ResendOTP,name='resendotp'),
    path('viewotp',views.ViewOTP,name='viewotp'),
    path('ListofApplicants', views.ListofApplicants, name='ListofApplicants'),
    
]
