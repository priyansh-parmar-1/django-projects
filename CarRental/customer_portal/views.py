from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from .models import *
from django.http import HttpResponse


# Create your views here.

def home(request):
    return render(request, 'index.html')

#adding  views
def about(request):
    return render(request, "about.html")

def booking(request):
    return render(request, "booking.html")

def service(request):
    return render(request, "service.html")

def contact(request):
    return render(request, "contact.html")

def detail(request):
    return render(request, "detail.html")


def car(request):
    return render(request, "car.html")


#=======
def login(request):

    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('pass')

        cust_obj = Customer.objects.get(email=uname)
        if cust_obj.email == uname:
            if cust_obj.password == pass1:
                return redirect('home')
            else:
                # return HttpResponse("Username or password incorrect")
                return render(request, 'login.html', {'msg': "Username or password incorrect"})
    return render(request,'login.html')

def signup(requst):
    if requst.method == 'POST':
        uname = requst.POST.get('username')
        email = requst.POST.get('email')
        pass1 = requst.POST.get('password1')
        new_cust = Customer(name=uname, email=email, password= pass1, is_verified=1)
        new_cust.save()
        print('user created')
        return redirect('login')
    return render(requst,'signup.html')

def logout(requst):
    user_logout(requst)
    return redirect('login')