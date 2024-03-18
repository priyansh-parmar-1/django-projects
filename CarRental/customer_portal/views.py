from django.shortcuts import render, redirect,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from .models import *
from django.http import HttpResponse
from .models import Customer
import re  # Import regular expression module
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.http import HttpResponseRedirect
from django.urls import reverse


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
            if cust_obj:
                if int(cust_obj.otp) != int(0):
                    otp = int(''.join(random.choices(string.digits, k=6)))
                    cust_obj.otp = otp
                    cust_obj.save()
                    message = """Thank you 🙏 for choosing CAR CASTLE. 
                           Please varify your email address by entering opt: """ + str(otp) + """ in verifation form."""
                    send_mail('Email varification OTP', message, 'settings.EMAIL_HOST_USER',
                              [uname], fail_silently=False)
                    return render(request, 'verifyotp.html', {'email': uname})
                elif str(cust_obj.password) == str(pass1):
                    request.session['cust_id'] = cust_obj.cust_id
                    request.session['cust_email'] = cust_obj.email
                    return redirect('home')
                else:
                    return render(request, 'login.html', {'msg': "Email or password incorrect",'isError':1, "uname": uname, "pass1": pass1})
    except Customer.DoesNotExist:
        return render(request, 'login.html', {'msg': "Customer does not exist",'isError':1, "uname": uname, "pass1": pass1})
    return render(request, 'login.html')

def verifyotp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        if email is not None and email is not '':
            cust_obj = Customer.objects.get(email=email, otp=otp)
            if cust_obj:
                cust_obj.otp = 0
                cust_obj.save()
                return render(request, 'login.html', {'msg': "OTP verified successfully", 'isError': 0})
            else:
                return render(request, 'verifyotp.html', {'msg': "Invalid otp"})
    return render(request, 'verifyotp.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            cust_obj = Customer.objects.get(email=email)
            if cust_obj.email == email:
                return render(request, 'signup.html', {'msg': "Email already exist"})
        except:
            pass
        otp = int(''.join(random.choices(string.digits, k=6)))
        uname = request.POST.get('username')
        pass1 = request.POST.get('password1')
        phone = request.POST.get('phone')
        dl_no = request.POST.get('dl')
        add = request.POST.get('address')
        dl_image = request.FILES.get('dl_image')
        cust_image = request.FILES.get('cust_image')
        message = """Thank you 🙏 for choosing CAR CASTLE. 
        Please varify your email address by entering opt: """ + str(otp) + """ in verifation form."""
        send_mail('Email varification OTP', message, 'settings.EMAIL_HOST_USER',
                  [email], fail_silently = False)
        new_cust = Customer(name=uname, email=email, password=pass1, is_verified=0, otp=otp, phone_no=phone, dl_no=dl_no, address=add, dl_image=dl_image, cust_image=cust_image)
        new_cust.save()
        return render(request, 'verifyotp.html', {'email': email})
    return render(request, 'signup.html')



# adding code for forgot password
# def changePassword(request):
#     return render(request,'change-password.html')



#     except Exception as e:
#         print(e)
#     return render(request,'forget-password.html')


def logout(request):
    user_logout(request)
    return redirect('home')

def cars(request):
    car = Car.objects.all()
    cust_id = request.session.get('cust_id')
    return render(request, 'cars.html', {'cars': car, 'cust_id': cust_id})


def carDetails(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    msg = request.session.pop('feedback_success_msg', None)
    feedback_list = Feedback.objects.filter(car_id=car_id)

    # Fetching customer names for each feedback
    feedback_details = []
    for feedback in feedback_list:
        customer = Customer.objects.get(cust_id=feedback.cust_id)
        feedback_details.append({'customer_name': customer.name,'customer_image': customer.cust_image.url, 'feedback_description': feedback.description})
    
    return render(request, 'carDetails.html', {'cars': [car], 'msg': msg, 'feedback_details': feedback_details})
    
    # return render(request, 'carDetails.html', {'cars': [car],'msg': msg})



def booking(request):
    car = Car.objects.all()
    cust_id = request.session.get('cust_id')
    return render(request, 'carDetails.html', {'cars': [car], 'cust_id': cust_id})

def booking(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    cust_id = request.session.get('cust_id')
    return render(request,'booking.html', {'cars': [car], 'cust_id': cust_id})

def profile(request):
    cust_id =request.session.get('cust_id')
    cust_obj = Customer.objects.get(cust_id=cust_id)
    if request.method == 'POST':
        email = request.POST.get('email')
        uname = request.POST.get('username')
        phone = request.POST.get('phone')
        dl_no = request.POST.get('dl')
        add = request.POST.get('address')
        dl_image = request.FILES.get('dl_image')
        cust_image = request.FILES.get('cust_image')
        pass1 = cust_obj.password
        if cust_image == None or cust_image == '':
            cust_image = cust_obj.cust_image
        if dl_image == None or dl_image == '':
            dl_image = cust_obj.dl_image
        if email == None or email == '':
            email = cust_obj.email
        new_cust = Customer(cust_id=cust_id ,name=uname, email=email, phone_no=phone,password=pass1, dl_no=dl_no, address=add, dl_image=dl_image, cust_image=cust_image)
        new_cust.save()
        cust_obj = Customer.objects.get(cust_id=cust_id)
    return render(request, 'profile.html', {'cust': cust_obj, 'cust_id': cust_id})



def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            cust_obj = Customer.objects.get(email=email)
            if cust_obj.cust_id == 0:
                return render(request, 'forgotPassword.html',{'msg': 'Please enter correct email, user not found with given email address'})
        except :
            return render(request, 'forgotPassword.html',{'msg': """Please enter correct email, 
            user not found with given email address"""})

        email = request.POST['email']
        all_characters = string.ascii_letters + string.digits
        password = ''.join(random.choices(all_characters, k=10))
        message = """Hello from car castle,  
        Your new generated password is: """ + password

        cust_obj = Customer.objects.get(email=email)
        cust_obj.password = password
        cust_obj.save()
        send_mail('Contact Form', message, 'settings.EMAIL_HOST_USER',
                  [email], fail_silently = False)
        return render(request, 'forgotPassword.html',{'msg': 'We have sent you email to change password'})
    return render(request ,'forgotPassword.html')



# adding for feedback


from django.http import HttpResponseRedirect
from django.urls import reverse

def submit_feedback(request):
    if request.method == 'POST':
        # Retrieve cust_id from session
        cust_id = request.session.get('cust_id')

        # Retrieve the car_id and feedback message from the form
        car_id = request.POST.get('car_id')
        description = request.POST.get('feedback-message')
        
        # Check if cust_id and car_id are available
        if cust_id and car_id:
            try:
                # Create a Feedback object with cust_id, car_id, and description
                feedback = Feedback.objects.create(cust_id=cust_id, car_id=car_id, description=description)
                messages.success(request, 'Feedback submitted successfully!')
            except Exception as e:
                messages.error(request, f'Error occurred while submitting feedback: {str(e)}')
        else:
            messages.error(request, 'Unable to submit feedback. Please log in first.')
        
        # Redirect to the car detail page
        return HttpResponseRedirect(reverse('carDetails', kwargs={'car_id': car_id}) + '?msg=Feedback+submitted+successfully')

    # If request method is not POST, render the car detail page
    return render(request, 'carDetails.html')
