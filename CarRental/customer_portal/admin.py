from django.contrib import admin
from . import models
from django.utils.html import format_html
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib import styles
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter,landscape
from reportlab.platypus import SimpleDocTemplate,Table, TableStyle,Spacer

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
    # search_fields=('car','cust',)
    list_filter=('car',)


# download booking report
    def draw_scrollbar(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(0.3)
        canvas.line(30, 30, doc.width - 10, 10)  # Adjust the y-coordinate for the position of the scrollbar
        canvas.restoreState()


    def download_report_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="booking_report.pdf"'

        # Create PDF content using ReportLab
        # pdf = SimpleDocTemplate(response, pagesize=landscape(letter)).
        pdf = SimpleDocTemplate(response, pagesize=landscape(letter), rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=50)

        elements = []

        # Table data
        data = [[" ID  ", "Car", "Customer", "Amount", "Pickup Address", "Drop Address", "Status", "Start Date Time", "End Date Time", "Pickup Pincode", "Drop Pincode"]]
        for booking in queryset:
            data.append([
                booking.booking_id, 
                booking.car, 
                booking.cust, 
                booking.amt, 
                booking.pick_add, 
                booking.drop_add, 
                booking.status, 
                booking.start_date_time, 
                booking.end_date_time, 
                booking.pick_pincode, 
                booking.drop_pincode
            ])

        # col_widths = [max([len(str(row[i])) * 7 for row in data]) for i in range(len(data[0]))]
        # table = Table(data, colWidths=col_widths)

        # # Create table
        # table = Table(data)
            
            # Calculate column widths dynamically based on content
        col_widths = [max([len(str(row[i])) * 4.3 for row in data]) for i in range(len(data[0]))]

        # Adjust font size if needed
        font_size = 6.5 if max(col_widths) > 100 else 10

        # Create table with adjusted column widths and font size
        table = Table(data, colWidths=col_widths)

        # Add style to table
        style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ('FONTSIZE', (0, 0), (-1, -1), font_size),])
        table.setStyle(style)

        # Add table to PDF elements
        elements.append(table)

        # pdf.multiBuild(elements, canvasmaker=draw_scrollbar)/
        # Build PDF
        pdf.build(elements)

        return response

    download_report_pdf.short_description = "Download Report PDF"

    actions = ['download_report_pdf']

# admin.site.register(YourModel, YourModelAdmin)


# ending download report



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('cust_id','image','name','phone_no','email','dl_no','address','drivinglicense','is_verified')
    list_filter=('name','email',)

    def image(self,obj):
        return format_html('<img src="{0}" width="auto" height="100px">'.format(obj.cust_image.url))
    def drivinglicense(self,obj):
        return format_html('<img src="{0}" width="auto" height="100px">'.format(obj.dl_image.url))

@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = models.Area.DisplayFields
    search_fields=('area_name','pincode',)

@admin.register(models.Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('car_id','company','registration_no','image','model_year','is_manual','mileage','is_diesel','car_type','model_name','capacity','color','charge')
    search_fields=('company',)
    list_filter=('company','model_year','is_manual','is_diesel','color')

    def image(self,obj):
        return format_html('<img src="{0}" width="auto" height="100px">'.format(obj.car_image.url))

@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_id','cust','car','description')
    search_fields=('cust','car',)

    def get_actions(self, request):
        # Disable all actions
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions
    
    
    def has_add_permission(self, request):
        # Disable add permission
        return False

@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_id','company_name')
    search_fields=('company_name',)