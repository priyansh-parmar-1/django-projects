from django.contrib import admin
from . import models
from django.utils.html import format_html
# Register your models here.
#admin.site.register(models.Customer)
#admin.site.register(models.Booking)
#admin.site.register(models.Car)
#admin.site.register(models.Area)
#admin.site.register(models.Company)
#admin.site.register(models.Feedback)
admin.site.register(models.Payment)

@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = models.Booking.DisplayFields

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('cust_id','image','name','phone_no','email','dl_no','address','drivinglicense','is_verified')

    def image(self,obj):
        return format_html('<img src="{0}" width="auto" height="100px">'.format(obj.cust_image.url))
    def drivinglicense(self,obj):
        return format_html('<img src="{0}" width="auto" height="100px">'.format(obj.dl_image.url))

@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = models.Area.DisplayFields

@admin.register(models.Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('car_id','company','registration_no','image','model_year','is_manual','mileage','is_diesel','car_type','model_name','capacity','color','charge')

    def image(self,obj):
        return format_html('<img src="{0}" width="auto" height="100px">'.format(obj.car_image.url))

@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_id','cust','car','description')

@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_id','company_name')