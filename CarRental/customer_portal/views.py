from django.shortcuts import render, redirect,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from .models import *
from django.http import HttpResponse
from .models import Customer
import re  # Import regular expression module
from django.contrib import messages



# Create your views here.

def home(request):
    car = Car.objects.all()
    cust_id =request.session.get('cust_id')
    return render(request, 'index.html', {'cars': car, 'cust_id': cust_id})


def login(request):
    try:
        if request.method == 'POST':
            uname = request.POST.get('username')
            pass1 = request.POST.get('pass')
            cust_obj = Customer.objects.get(email=uname)
            if cust_obj.email == uname:
                if cust_obj.password == pass1:
                    request.session['cust_id'] = cust_obj.cust_id
                    request.session['cust_email'] = cust_obj.email
                    return redirect('home')
                else:
                    return render(request, 'login.html', {'msg': "Email or password incorrect", "uname": uname, "pass1": pass1})
    except Customer.DoesNotExist:
        return render(request, 'login.html', {'msg': "Customer does not exist", "uname": uname, "pass1": pass1})
    return render(request, 'login.html')



def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            cust_obj = Customer.objects.get(email=email)
            if cust_obj.email == email:
                return render(request, 'signup.html', {'msg': "Email already exist"})
        except:
            pass
        uname = request.POST.get('username')
        pass1 = request.POST.get('password1')
        phone = request.POST.get('phone')
        dl_no = request.POST.get('dl')
        add = request.POST.get('address')
        dl_image = request.FILES.get('dl_image')
        cust_image = request.FILES.get('cust_image')
        new_cust = Customer(name=uname, email=email, password=pass1, is_verified=0, phone_no=phone, dl_no=dl_no, address=add, dl_image=dl_image, cust_image=cust_image)
        new_cust.save()
        print('user created')
        return redirect('login')
    return render(request, 'signup.html')


# adding code for forgot password
# def changePassword(request):
#     return render(request,'change-password.html')

# def ForgetPassword(request):
#     try:
#         if request.method == 'POST':
#             uname=request.POST.get('username')

#             if not  Customer.objects.get(email=uname).first():
#                 messages.success(request,'No User Found with this username')
#                 return redirect('/forget-password')
            
#             cust_obj=Customer.objects.get(email=uname)

             

#     except Exception as e:
#         print(e)
#     return render(request,'forget-password.html')


def logout(request):
    user_logout(request)
    return redirect('home')

def cars(request):
    car = Car.objects.all()
    return render(request, 'cars.html', {'cars': car})


def carDetails(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, 'carDetails.html', {'cars': [car]})



def booking(request):
    car = Car.objects.all()
    cust_id = request.session.get('cust_id')
    return render(request,'booking.html', {'cars': car, 'cust_id': cust_id})


