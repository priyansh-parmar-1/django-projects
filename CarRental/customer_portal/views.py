from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from .models import *
from django.http import HttpResponse, JsonResponse
from .models import Customer
import re  # Import regular expression module
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
import string
import razorpay
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import pytz


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# Create your views here.

def home(request):
    car = Car.objects.all()[:6]
    cust_id = request.session.get('cust_id')
    return render(request, 'index.html', {'cars': car, 'cust_id': cust_id})

def about(request):
    cust_id = request.session.get('cust_id')
    return render(request, 'about.html', {'cust_id': cust_id})

def contact(request):
    cust_id = request.session.get('cust_id')
    return render(request, 'contact.html', {'cust_id': cust_id})

def terms(request):
    cust_id = request.session.get('cust_id')
    return render(request, 'terms_conditions.html', {'cust_id': cust_id})

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
                           Please varify your email address by entering opt: """ + str(
                        otp) + """ in verification form."""
                    send_mail('Email varification OTP', message, 'settings.EMAIL_HOST_USER',
                              [uname], fail_silently=False)
                    return render(request, 'verifyotp.html', {'email': uname})
                elif str(cust_obj.password) == str(pass1):
                    request.session['cust_id'] = cust_obj.cust_id
                    request.session['cust_email'] = cust_obj.email
                    return redirect('home')
                else:
                    return render(request, 'login.html',
                                  {'msg': "Email or password incorrect", 'isError': 1, "uname": uname, "pass1": pass1})
    except Customer.DoesNotExist:
        return render(request, 'login.html',
                      {'msg': "Customer does not exist", 'isError': 1, "uname": uname, "pass1": pass1})
    return render(request, 'login.html')

def changepassword(request):
    cust_id = request.session.get('cust_id')
    try:
        if request.method == 'POST':
            cust_id = request.session.get('cust_id')
            currPass = request.POST.get('currPass')
            newPass = request.POST.get('newPass')
            cust_obj = Customer.objects.get(cust_id=cust_id)
            if cust_obj:
                if cust_obj.password == currPass:
                    cust_obj.password = newPass
                    cust_obj.save()
                    return render(request, 'changepassword.html',
                                  {'msg': 'Password updated successfully', 'isError': 0, 'cust_id': cust_id})
                else:
                    return render(request, 'changepassword.html',
                                  {'msg': 'Incorrect password', 'isError': 1, 'cust_id': cust_id})
    except:
        pass
    return render(request, 'changepassword.html', {'cust_id': cust_id})

def verifyotp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        if email != None and email != '':
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
                  [email], fail_silently=False)
        new_cust = Customer(name=uname, email=email, password=pass1, is_verified=0, otp=otp, phone_no=phone,
                            dl_no=dl_no, address=add, dl_image=dl_image, cust_image=cust_image)
        new_cust.save()
        return render(request, 'verifyotp.html', {'email': email})
    return render(request, 'signup.html')

def logout(request):
    user_logout(request)
    return redirect('home')

def cars(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        multipleQ = Q(Q(model_name__icontains=search) | Q(car_type__icontains=search) | Q(
            company__company_name__icontains=search))
        car = Car.objects.filter(multipleQ)
    else:
        car = Car.objects.all()
    cust_id = request.session.get('cust_id')
    return render(request, 'cars.html', {'cars': car, 'cust_id': cust_id})


def carDetails(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    cust_id = request.session.get('cust_id')
    msg = request.session.pop('feedback_success_msg', None)
    feedback_list = Feedback.objects.filter(car_id=car_id)

    # Fetching customer names for each feedback
    feedback_details = []
    for feedback in feedback_list:
        customer = Customer.objects.get(cust_id=feedback.cust_id)
        feedback_details.append({'customer_name': customer.name, 'customer_image': customer.cust_image.url,
                                 'feedback_description': feedback.description})

    booking = Booking.objects.filter(car_id=car_id,cust_id=cust_id,status_id=2)
    if booking:
        isbooked = 1
    else:
        isbooked = 0
    return render(request, 'carDetails.html',
                  {'cars': [car], 'cust_id': cust_id, 'msg': msg, 'isbooked':isbooked,'feedback_details': feedback_details})


def downloadinvoice(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    template = get_template('invoice.html')
    curdate = datetime.now()
    html = template.render({'booking': booking,'date': curdate})
    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    # If PDF generation failed, return error
    if pisa_status.err:
        return HttpResponse('PDF generation error.')
    return response


def booking(request, car_id):
    cust_id = request.session.get('cust_id')
    if cust_id == 0 or cust_id == None:
        return redirect('login')
    else:
        car = get_object_or_404(Car, pk=car_id)
        area = Area.objects.all()
        request.session['charge'] = car.charge
        request.session['car_id'] = car_id
    return render(request, 'booking.html', {'cars': [car], 'cust_id': cust_id, 'areas': area})


def view_bookings(request):
    cust_id = request.session.get('cust_id')
    if cust_id == 0 or cust_id == None:
        return redirect('login')
    if request.method == 'POST':
        fg = int(request.POST.get('flag'))
        if fg == 1:
            booking_id = request.POST.get('booking_id')
            bookings = Booking.objects.get(cust=cust_id, booking_id=booking_id)
            bookings.status_id = 4
            bookings.save()
            msg = "Booking cancelled successfully"
            bookings = Booking.objects.filter(cust=cust_id)
            now = timezone.now()
            for i in bookings:
                time_difference = i.start_date_time - now
                i.time = int(time_difference.total_seconds() / 3600)
            return render(request, 'view_bookings.html', {'bookings': bookings, 'msg': msg, 'cust_id': cust_id})
    else:
        bookings = Booking.objects.filter(cust=cust_id).order_by('-booking_date_time')
        now = timezone.now()
        for i in bookings:
            time_difference = i.start_date_time - now
            i.time = int(time_difference.total_seconds() / 3600)
        return render(request, 'view_bookings.html', {'bookings': bookings, 'cust_id': cust_id})

def profile(request):
    cust_id = request.session.get('cust_id')
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
        new_cust = Customer(cust_id=cust_id, name=uname, email=email, phone_no=phone, password=pass1, dl_no=dl_no,
                            address=add, dl_image=dl_image, cust_image=cust_image)
        new_cust.save()
        cust_obj = Customer.objects.get(cust_id=cust_id)
    return render(request, 'profile.html', {'cust': cust_obj, 'cust_id': cust_id})

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            cust_obj = Customer.objects.get(email=email)
            if cust_obj.cust_id == 0:
                return render(request, 'forgotPassword.html',
                              {'msg': 'Please enter correct email, user not found with given email address'})
        except:
            return render(request, 'forgotPassword.html', {'msg': """Please enter correct email, 
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
                  [email], fail_silently=False)
        return render(request, 'forgotPassword.html', {'msg': 'We have sent you email to change password'})
    return render(request, 'forgotPassword.html')
# adding for feedback

def submit_feedback(request):
    cust_id = request.session.get('cust_id')
    if request.method == 'POST':
        # Retrieve cust_id from session
        if cust_id == 0 and cust_id == None:
            return redirect('login')

        # Retrieve the car_id and feedback message from the form
        car_id = request.POST.get('car_id')
        description = request.POST.get('feedback-message')

        # Check if cust_id and car_id are available
        if cust_id and car_id:
            try:
                # Create a Feedback object with cust_id, car_id, and description
                feedback = Feedback.objects.create(cust_id=cust_id, car_id=car_id, description=description)
                feedback.save()
                messages.success(request, 'Feedback submitted successfully!')
            except Exception as e:
                messages.error(request, f'Error occurred while submitting feedback: {str(e)}')
        else:
            messages.error(request, 'Unable to submit feedback. Please log in first.')

        # Redirect to the car detail page
        return HttpResponseRedirect(
            reverse('carDetails', kwargs={'car_id': car_id}) + '?msg=Feedback+submitted+successfully')

    # If request method is not POST, render the car detail page
    return render(request, 'carDetails.html',{'cust_id':cust_id})

def payment(request):
    if request.method == "POST":
        pick_date_time_str = request.POST.get('pickupdate')
        request.session['pick_date'] = pick_date_time_str
        drop_date_time_str = request.POST.get('dropdate')
        request.session['drop_date'] = drop_date_time_str
        pick_date_time = datetime.strptime(pick_date_time_str, '%Y-%m-%dT%H:%M')
        drop_date_time = datetime.strptime(drop_date_time_str, '%Y-%m-%dT%H:%M')
        charge = request.session.get('charge')
        flag = request.POST.get('flag')
        request.session['flag'] = flag
        print(charge)

        time_difference = drop_date_time - pick_date_time
        print(time_difference)
        total_hours = time_difference.total_seconds() / 3600

        print(total_hours)
        amt = round(total_hours * charge, 2) + 5000
        request.session['amt'] = amt
        print(amt)
        car_id = request.session.get('car_id')
        car = get_object_or_404(Car, pk=car_id)
        bk = Booking.objects.filter(car=car, end_date_time__gt=pick_date_time_str, status_id=1)

        if bk.exists():
            # If there's an existing booking with end_date_time later than pick_date_time
            msg = 'Cannot make booking. Overlapping with existing booking From: ' + bk[0].start_date_time.strftime(
                "%Y-%m-%d %H:%M:%S") + ' To: ' + bk[0].end_date_time.strftime("%Y-%m-%d %H:%M:%S")
            return render(request, 'booking_error.html',
                          {'alert_message': msg, 'car': car})
        # Create a Razorpay Order
        client = razorpay.Client(
            auth=("rzp_test_zL6UJeuzbo8rNk", "7X6pSHXakyjGlGdYvGmZ95zt"))
        razorpay_order = client.order.create(
            {'amount': int(amt)*100,
             'currency': 'INR',
             'payment_capture': "1"
             }
        )
        order_id = razorpay_order['id']
        request.session['order_id'] = order_id
        drop_code = request.POST.get('drop_pincode')
        request.session['drop_code'] = drop_code
        pick_code = request.POST.get('pickup_pincode')
        request.session['pick_code'] = pick_code
        drop_area = get_object_or_404(Area, pk=drop_code)
        pick_area = get_object_or_404(Area, pk=pick_code)
        pick_location = request.POST.get('pickuplocation')
        request.session['pick_location'] = pick_location
        drop_location = request.POST.get('droplocation')
        request.session['drop_location'] = drop_location


        cust_id = request.session.get('cust_id')
        charge = request.session.get('charge')
        cust_obj = Customer.objects.get(cust_id=cust_id)
    return render(request, 'payment.html',{'amt': amt, "order_id": order_id, 'cust': cust_obj})

def proceedToPay(request):
    amt = request.session.get('amt')
    return JsonResponse({
        'amount': amt
    })
@csrf_exempt
def confirm_booking(request):
    cust_id = request.session.get('cust_id')
    if cust_id == 0 and cust_id == None:
        return redirect('login')
    else:
        drop_code = request.session.get('drop_code')
        pick_code = request.session.get('pick_code')
        drop_area = get_object_or_404(Area, pk=drop_code)
        pick_area = get_object_or_404(Area, pk=pick_code)
        pick_location = request.session.get('pick_location')
        drop_location = request.session.get('drop_location')
        pick_date_time_str = request.session.get('pick_date')
        drop_date_time_str = request.session.get('drop_date')
        car_id = request.session.get('car_id')
        car = get_object_or_404(Car, pk=car_id)
        cust_id = request.session.get('cust_id')
        cust_obj = get_object_or_404(Customer, pk=cust_id)
        amt = request.session.get('amt')
        payment_id = request.POST.get('payment_id')
        bk = Booking.objects.filter(car=car, end_date_time__gt=pick_date_time_str, status_id=1)

        if bk.exists():
            # If there's an existing booking with end_date_time later than pick_date_time
            msg = 'Cannot make booking. Overlapping with existing booking From: ' + bk[0].start_date_time.strftime(
                "%Y-%m-%d %H:%M:%S") + ' To: ' + bk[0].end_date_time.strftime("%Y-%m-%d %H:%M:%S")
            return render(request, 'booking_error.html',
                          {'alert_message': msg, 'car': car})
        date = datetime.now()
        booking_obj = Booking(car=car, cust_id=cust_id, amt=amt, pick_add=pick_location, drop_add=drop_location,
                              status_id=1, start_date_time=pick_date_time_str, end_date_time=drop_date_time_str,
                              pick_pincode=pick_area, drop_pincode=drop_area, time=0,booking_date_time=date)
        booking_obj.save()
        payment_obj = Payment(booking=booking_obj,cust=cust_obj,transaction=payment_id,status='paid',payment_date=date)
        payment_obj.save()
        msg = 'Booking confirmed'
        return render(request, 'view_bookings.html',
                      {'message': msg})
# ----------------------- VERIFY SIGNATURE  -----------------------------------


def success(request):
    return render(request, "payment-successful.html")
