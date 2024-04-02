from django.contrib import admin
from . import models
from django.utils.html import format_html
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib import styles
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter,landscape
from reportlab.platypus import SimpleDocTemplate,Table, TableStyle,Spacer,Paragraph
from reportlab.lib.units import inch
from reportlab.platypus import Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from datetime import datetime
from reportlab.platypus import PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from django.conf import settings
import datetime
# from reportlab.platypus.frames import Frame, ShowBoundaryValue


# Register your models here.
#admin.site.register(models.Customer)
#admin.site.register(models.Booking)
#admin.site.register(models.Car)
#admin.site.register(models.Area)
#admin.site.register(models.Company)
#admin.site.register(models.Feedback)
#admin.site.register(models.Payment)
#admin.site.register(models.bookingstatus)

# report for payment

# @admin.payment(models.Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display=models.Payment.DisplayFields

#     def download_report_pdf(self, request, queryset):
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="payment_report.pdf"'

#         # Create PDF content using ReportLab
        #   pdf = SimpleDocTemplate(response, pagesize=landscape(letter), rightMargin=10, leftMargin=10, topMargin=20, bottomMargin=50)
#         elements = []

                # Get the current date and time
        # current_date = datetime.datetime.now().strftime("Report date  : "+"%Y/%m/%d ")
        # # current_date = datetime.datetime.now().strftime("Report date  : "+"%Y/%m/%d  %H:%M:%S")

        # # Add the current date to the PDF elements
        # current_date_paragraph = Paragraph(current_date, getSampleStyleSheet()["BodyText"])
        # elements.append(current_date_paragraph)




            # Define a custom Paragraph style with centered alignment
        # centered_style = ParagraphStyle(
        #     name='CenteredHeading',
        #     parent=getSampleStyleSheet()["Heading1"],
        #     alignment=TA_CENTER
        # )

        # # Define the path to your image file
        # image_path = settings.MEDIA_ROOT + '/img/logo-no-background.png'
        # # Add the image to the PDF elements
        # image = Image(image_path, width=200, height=30)  # Adjust width and height as needed
        # elements.append(image)
        # # Define the margin after the image
        # margin_after_image = 40
        # Add a Spacer element to create

#         # Table data
#         data = [["Payment ID", "Booking ID", "Customer", "Transaction", "Status", "Payment Date"]]
#         for payment in queryset:
#             data.append([
#                 payment.payment_id,
#                 payment.booking.booking_id,
#                 payment.cust.name,
#                 payment.transaction,
#                 payment.status,
#                 payment.payment_date.strftime("Report Date : "+"%Y-%m-%d ")
#                 payment.payment_date.strftime("%Y-%m-%d %H:%M:%S")
#             ])

#         # Calculate column widths dynamically based on content
#         col_widths = [max([len(str(row[i])) * 3.5 for row in data]) for i in range(len(data[0]))]

#         # Create table with adjusted column widths
#         table = Table(data, colWidths=col_widths)

#         # Add style to table
#         style = TableStyle([
#             ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#             ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('FONTSIZE', (0, 0), (-1, -1), 10),
#         ])
#         table.setStyle(style)

#         # Add table to PDF elements
#         elements.append(table)

#         # Build PDF
#         pdf.build(elements)

#         return response

#     download_report_pdf.short_description = "Download Payment Report PDF"

#     actions = ['download_report_pdf']

# =========================================================================================

@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = models.Booking.DisplayFields
    list_filter=('car','booking_date_time')

    list_display = ('booking_id','car','cust','amt','pick_add','drop_add','status','start_date_time','end_date_time','pick_pincode','drop_pincode','booking_date_time')
    # search_fields=('car','cust',)
    readonly_fields = ('booking_id','car','cust','amt','pick_add','drop_add','start_date_time','end_date_time','pick_pincode','drop_pincode','booking_date_time','time')
    list_filter=('car','cust','status','booking_date_time')


    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj and obj.status_id == 2 or obj.status_id == 4 or obj.status_id == 5:
            readonly_fields += ('status',)
        return readonly_fields
    def download_report_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="booking_report.pdf"'
        pdf = SimpleDocTemplate(response, pagesize=landscape(letter), rightMargin=10, leftMargin=10, topMargin=20, bottomMargin=50)

        elements = []

        
        # Get the current date and time
        current_date = datetime.datetime.now().strftime("Report date  : "+"%Y/%m/%d ")
        # current_date = datetime.datetime.now().strftime("Report date  : "+"%Y/%m/%d  %H:%M:%S")

        # Add the current date to the PDF elements
        current_date_paragraph = Paragraph(current_date, getSampleStyleSheet()["BodyText"])
        elements.append(current_date_paragraph)


# Define a custom Paragraph style with centered alignment
        centered_style = ParagraphStyle(
            name='CenteredHeading',
            parent=getSampleStyleSheet()["Heading1"],
            alignment=TA_CENTER
        )

        # Define the path to your image file
        image_path = settings.MEDIA_ROOT + '/img/logo-no-background.png'
        # Add the image to the PDF elements
        image = Image(image_path, width=200, height=30)  # Adjust width and height as needed
        elements.append(image)
        # Define the margin after the image
        margin_after_image = 40
        # Add a Spacer element to create the margin after the image
        elements.append(Spacer(4, margin_after_image))
        # Add heading to the PDF using the centered style
        # header1 = Paragraph("<b>Car Castle</b>", centered_style)
        header = Paragraph("<b>Booking Report</b>", centered_style)
        # elements.append(header1)
        elements.append(header)
        elements.append(Paragraph("<br/>", getSampleStyleSheet()["BodyText"]))

        # Table data
        data = [[" ID  ", "Car", "Customer", "   Amount  ", "Pickup Address", "Drop Address", " Status     ", "Start Date Time", "End Date Time", "Pickup Pincode", "Drop Pincode"]]
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

        # Calculate column widths dynamically based on content
        col_widths = [max([len(str(row[i])) * 3.4 for row in data]) for i in range(len(data[0]))]

        # Adjust font size if needed
        font_size = 5.5 if max(col_widths) > 100 else 10

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

        # Build PDF
        pdf.build(elements)

        return response

    download_report_pdf.short_description = "Download Report PDF"

    actions = ['download_report_pdf']
# admin.site.register(YourModel, YourModelAdmin)


# ending download report

# ==========================================================

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('cust_id','image','name','dl_image','cust_image','otp','password','phone_no','email','dl_no','address','drivinglicense','is_verified')
    list_filter=('name','email',)
    readonly_fields = tuple(field for field in list_display if field != 'is_verified')
    # it is for hiding the password field
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)
        else:
            return (
                (None, {'fields': ('cust_id', 'name', 'phone_no', 'email', 'dl_no', 'address', 'is_verified')}),
            )
    def image(self,obj):
        return format_html('<img src="{0}" width="auto" height="100px">'.format(obj.cust_image.url))
    def drivinglicense(self,obj):
        return format_html('<img src="{0}" width="auto" height="100px">'.format(obj.dl_image.url))
    # adding report here

    def generate_customer_report(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="customer_report.pdf"'

        # Create PDF content using ReportLab
        # pdf = SimpleDocTemplate(response, pagesize=letter)
        pdf = SimpleDocTemplate(response, pagesize=landscape(letter), rightMargin=10, leftMargin=10, topMargin=20, bottomMargin=50)

        elements = []

         
        # Get the current date and time
        current_date = datetime.datetime.now().strftime("Report Date: "+"%Y-%m-%d ")
        # current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add the current date to the PDF elements
        current_date_paragraph = Paragraph(current_date, getSampleStyleSheet()["BodyText"])
        elements.append(current_date_paragraph)


# Define a custom Paragraph style with centered alignment
        centered_style = ParagraphStyle(
            name='CenteredHeading',
            parent=getSampleStyleSheet()["Heading1"],
            alignment=TA_CENTER
        )

        # Define the path to your image file
        image_path = settings.MEDIA_ROOT + '/img/logo-no-background.png'
        # Add the image to the PDF elements
        image = Image(image_path, width=200, height=30)  # Adjust width and height as needed
        elements.append(image)
        # Define the margin after the image
        margin_after_image = 40
        # Add a Spacer element to create the margin after the image
        elements.append(Spacer(4, margin_after_image))
        # Add heading to the PDF using the centered style
        # header1 = Paragraph("<b>Car Castle</b>", centered_style)
        header = Paragraph("<b>Customer Report</b>", centered_style)
        # elements.append(header1)
        elements.append(header)
        elements.append(Paragraph("<br/>", getSampleStyleSheet()["BodyText"]))


        # Table data
        data = [["ID", "Name", "Phone No", "Email", "DL No", "Address", "Verified"]]
        for customer in queryset:
            data.append([
                customer.cust_id, 
                customer.name, 
                customer.phone_no, 
                customer.email, 
                customer.dl_no, 
                customer.address, 
                "Yes" if customer.is_verified else "No"
            ])

                    # Calculate column widths dynamically based on content
            col_widths = [max([len(str(row[i])) * 3.4 for row in data]) for i in range(len(data[0]))]

            # Adjust font size if needed
            font_size = 4.5 if max(col_widths) > 100 else 10

        # Create table
        table = Table(data)

        # Add style to table
        style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(style)

        # Add table to PDF elements
        elements.append(table)

        # Build PDF
        pdf.build(elements)

        return response

    generate_customer_report.short_description = "Generate Customer Report"

    actions = ['generate_customer_report']
# =================================================================================
@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = models.Area.DisplayFields
    search_fields=('area_name','pincode',)

    
    def download_report_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="area_report.pdf"'

        # Create PDF content using ReportLab
        # pdf = SimpleDocTemplate(response, pagesize=letter)
        pdf = SimpleDocTemplate(response, pagesize=landscape(letter), rightMargin=10, leftMargin=10, topMargin=20, bottomMargin=50)

        elements = []
         
        # Get the current date and time
        current_date = datetime.datetime.now().strftime("Report Date : "+"%Y-%m-%d")
        # current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add the current date to the PDF elements
        current_date_paragraph = Paragraph(current_date, getSampleStyleSheet()["BodyText"])
        elements.append(current_date_paragraph)


# Define a custom Paragraph style with centered alignment
        centered_style = ParagraphStyle(
            name='CenteredHeading',
            parent=getSampleStyleSheet()["Heading1"],
            alignment=TA_CENTER
        )

        # Define the path to your image file
        image_path = settings.MEDIA_ROOT + '/img/logo-no-background.png'
        # Add the image to the PDF elements
        image = Image(image_path, width=200, height=30)  # Adjust width and height as needed
        elements.append(image)
        # Define the margin after the image
        margin_after_image = 40
        # Add a Spacer element to create the margin after the image
        elements.append(Spacer(4, margin_after_image))
        # Add heading to the PDF using the centered style
        # header1 = Paragraph("<b>Car Castle</b>", centered_style)
        header = Paragraph("<b>Area Report</b>", centered_style)
        # elements.append(header1)
        elements.append(header)
        elements.append(Paragraph("<br/>", getSampleStyleSheet()["BodyText"]))


        # Table data
        data = [["Pincode     ", "Area Name                 "]]
        for area in queryset:
            data.append([area.pincode, area.area_name])

        # Calculate column widths dynamically based on content
        col_widths = [max([len(str(row[i])) * 6 for row in data]) for i in range(len(data[0]))]

        # Create table with adjusted column widths
        table = Table(data, colWidths=col_widths)

        # Add style to table
        style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ])
        table.setStyle(style)

        # Add table to PDF elements
        elements.append(table)

        # Build PDF
        pdf.build(elements)

        return response

    download_report_pdf.short_description = "Download Area Report PDF"

    actions = ['download_report_pdf']



# ================================================================

@admin.register(models.Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('car_id','company','registration_no','image','model_year','is_manual','mileage','is_diesel','car_type','model_name','capacity','color','charge')
    # search_fields=('company',)
    list_filter=('company','model_year','is_manual','is_diesel','color')

    def image(self,obj):
        return format_html('<img src="{0}" width="auto" height="100px">'.format(obj.car_image.url))

    def download_report_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="car_report.pdf"'

        # Create PDF content using ReportLab
        pdf = SimpleDocTemplate(response, pagesize=landscape(letter), rightMargin=10, leftMargin=10, topMargin=20, bottomMargin=50)
        elements = []
         
        # Get the current date and time
        current_date = datetime.datetime.now().strftime("Report Date :"+"%Y-%m-%d ")
        # current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add the current date to the PDF elements
        current_date_paragraph = Paragraph(current_date, getSampleStyleSheet()["BodyText"])
        elements.append(current_date_paragraph)


# Define a custom Paragraph style with centered alignment
        centered_style = ParagraphStyle(
            name='CenteredHeading',
            parent=getSampleStyleSheet()["Heading1"],
            alignment=TA_CENTER
        )

        # Define the path to your image file
        image_path = settings.MEDIA_ROOT + '/img/logo-no-background.png'
        # Add the image to the PDF elements
        image = Image(image_path, width=200, height=30)  # Adjust width and height as needed
        elements.append(image)
        # Define the margin after the image
        margin_after_image = 40
        # Add a Spacer element to create the margin after the image
        elements.append(Spacer(4, margin_after_image))
        # Add heading to the PDF using the centered style
        # header1 = Paragraph("<b>Car Castle</b>", centered_style)
        header = Paragraph("<b>Cars Report</b>", centered_style)
        # elements.append(header1)
        elements.append(header)
        elements.append(Paragraph("<br/>", getSampleStyleSheet()["BodyText"]))


        # Table data
        data = [[" ID  ","Car Image", "   Company   ", "Registration No  ", "Model Name  ", "Car Type  ", "Charge  "]]
        for car in queryset:
            data.append([
                car.car_id,
                Image(car.car_image.path, width=1*inch, height=1*inch)  ,
                car.company,
                car.registration_no,
                car.model_name,
                car.car_type,
                car.charge,

            ])

        # Calculate column widths dynamically based on content
        col_widths = [max([len(str(row[i])) * 4.9 for row in data]) for i in range(len(data[0]))]

        # Create table with adjusted column widths
        table = Table(data, colWidths=col_widths)

        # Add style to table
        style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ])
        table.setStyle(style)

        # Add table to PDF elements
        elements.append(table)

        # Build PDF
        pdf.build(elements)

        return response

    download_report_pdf.short_description = "Download Car Report PDF"

    actions = ['download_report_pdf']
# =======================================================================================================
@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_id','cust','car','description')
    # search_fields=('cust','car',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_customer_name(self, Customer):
        return Customer.cust.name if Customer.cust else ""
    get_customer_name.short_description = 'Customer'

    def get_car_name(self, Car):
        return Car.car.company if Car.car else ""
    get_car_name.short_description = 'Car'


    def generate_feedback_report(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="feedback_report.pdf"'

        # Create PDF content using ReportLab
        # pdf = SimpleDocTemplate(response, pagesize=letter)
        pdf = SimpleDocTemplate(response, pagesize=landscape(letter), rightMargin=10, leftMargin=10, topMargin=20, bottomMargin=50)

        elements = []
         
        # Get the current date and time
        current_date = datetime.datetime.now().strftime("Report Date : "+"%Y-%m-%d ")
        # current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add the current date to the PDF elements
        current_date_paragraph = Paragraph(current_date, getSampleStyleSheet()["BodyText"])
        elements.append(current_date_paragraph)


# Define a custom Paragraph style with centered alignment
        centered_style = ParagraphStyle(
            name='CenteredHeading',
            parent=getSampleStyleSheet()["Heading1"],
            alignment=TA_CENTER
        )

        # Define the path to your image file
        image_path = settings.MEDIA_ROOT + '/img/logo-no-background.png'
        # Add the image to the PDF elements
        image = Image(image_path, width=200, height=30)  # Adjust width and height as needed
        elements.append(image)
        # Define the margin after the image
        margin_after_image = 40
        # Add a Spacer element to create the margin after the image
        elements.append(Spacer(4, margin_after_image))
        # Add heading to the PDF using the centered style
        # header1 = Paragraph("<b>Car Castle</b>", centered_style)
        header = Paragraph("<b>Feedback Report</b>", centered_style)
        # elements.append(header1)
        elements.append(header)
        elements.append(Paragraph("<br/>", getSampleStyleSheet()["BodyText"]))


        # Table data
        data = [["Feedback ID", "Customer", "Car", "Description"]]
        for feedback in queryset:
            data.append([
                feedback.feedback_id, 
                self.get_customer_name(feedback),
                self.get_car_name(feedback),
                feedback.description
            ])

        # Create table
        table = Table(data)

        # Add style to table
        style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        table.setStyle(style)

        # Add table to PDF elements
        elements.append(table)

        # Build PDF
        pdf.build(elements)

        return response

    generate_feedback_report.short_description = "Generate Feedback Report"

    actions = ['generate_feedback_report']

    


    # ============================================================================

@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_id','company_name')
    search_fields=('company_name',)

    
    def download_report_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="company_report.pdf"'

        # Create PDF content using ReportLab
        # pdf = SimpleDocTemplate(response, pagesize=letter)
        pdf = SimpleDocTemplate(response, pagesize=landscape(letter), rightMargin=10, leftMargin=10, topMargin=20, bottomMargin=50)

        elements = []
         
        # Get the current date and time
        current_date = datetime.datetime.now().strftime("Report Date : "+"%Y-%m-%d ")
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add the current date to the PDF elements
        current_date_paragraph = Paragraph(current_date, getSampleStyleSheet()["BodyText"])
        elements.append(current_date_paragraph)


# Define a custom Paragraph style with centered alignment
        centered_style = ParagraphStyle(
            name='CenteredHeading',
            parent=getSampleStyleSheet()["Heading1"],
            alignment=TA_CENTER
        )

        # Define the path to your image file
        image_path = settings.MEDIA_ROOT + '/img/logo-no-background.png'
        # Add the image to the PDF elements
        image = Image(image_path, width=200, height=30)  # Adjust width and height as needed
        elements.append(image)
        # Define the margin after the image
        margin_after_image = 40
        # Add a Spacer element to create the margin after the image
        elements.append(Spacer(4, margin_after_image))
        # Add heading to the PDF using the centered style
        # header1 = Paragraph("<b>Car Castle</b>", centered_style)
        header = Paragraph("<b>Company Report</b>", centered_style)
        # elements.append(header1)
        elements.append(header)
        elements.append(Paragraph("<br/>", getSampleStyleSheet()["BodyText"]))


        # Table data
        data = [["  Company ID   ", "  Company Name  "]]
        for company in queryset:
            data.append([
                company.company_id,
                company.company_name
            ])

        # Calculate column widths dynamically based on content
        col_widths = [max([len(str(row[i])) * 6 for row in data]) for i in range(len(data[0]))]

        # Create table with adjusted column widths
        table = Table(data, colWidths=col_widths)

        # Add style to table
        style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ])
        table.setStyle(style)

        # Add table to PDF elements
        elements.append(table)

        # Build PDF
        pdf.build(elements)

        return response

    download_report_pdf.short_description = "Download Company Report PDF"

    actions = ['download_report_pdf']


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'booking', 'cust', 'transaction', 'status', 'payment_date')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
