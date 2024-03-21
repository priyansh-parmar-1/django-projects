"""
URL configuration for carRental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('login', login, name='login'),
    path('logout/', logout, name='logout'),
    path('cars/', cars, name='cars'),
    path('cars', cars, name='cars'),
    path('profile/', profile, name='profile'),
    path('changepassword/', changepassword, name='changepassword'),
    path('cars/<car_id>/', carDetails, name='carDetails'),
    path('submit_feedback/', submit_feedback, name='submit_feedback'),
    path('cars/<car_id>/', carDetails, name='carDetails'),
    path('booking/<car_id>/', booking, name='booking'),
    path('verifyotp', verifyotp, name='verifyotp'),
    path('forgotPassword/', forgotPassword, name='forgotPassword'),
    path('payment/', payment, name='payment'),
    path('viewbookings/', view_bookings, name='viewbookings'),
    path('viewbookings', view_bookings, name='viewbookings'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('terms/', terms, name='terms'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
