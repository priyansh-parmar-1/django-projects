from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.http import HttpResponse


# Create your views here.

def home(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('pass')

        user = authenticate(request,username=uname,password=pass1)
        if user is not None:
            user_login(request, user)
            return redirect('home')
        else:
           # return HttpResponse("Username or password incorrect")
           return render(request, 'login.html',{'msg':"Username or password incorrect"})
    return render(request,'login.html')

def signup(requst):
    if requst.method == 'POST':
        uname = requst.POST.get('username')
        email = requst.POST.get('email')
        pass1 = requst.POST.get('password1')
        new_cust = User.objects.create_user(uname, email, pass1)
        new_cust.save()
        print('user created')
        return redirect('login')
    return render(requst,'signup.html')

def logout(requst):
    user_logout(requst)
    return redirect('login')