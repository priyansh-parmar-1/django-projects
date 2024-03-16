from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Customer)
admin.site.register(models.Booking)
admin.site.register(models.Car)
admin.site.register(models.Area)
admin.site.register(models.Company)
admin.site.register(models.Feedback)
admin.site.register(models.Payment)