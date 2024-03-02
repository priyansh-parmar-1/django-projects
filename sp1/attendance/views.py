from django.shortcuts import render
from django.http import HttpResponse
from .models import Std
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    param = {
        'name' : 'django'
    }
    return render(request,'attendance/index.html',param)

def view_data(request):

    stds = Std.objects.all()
    context = {
        'stds':stds
    }
    '''attend=[
        {'rno': 85,'name':'Priyansh','status':'present'},
        {'rno': 117,'name':'Dhaval','status':'Absent'},
        {'rno': 79,'name':'Man','status':'present'}
    ]'''
    return render(request,'attendance/view_attendance.html',context)