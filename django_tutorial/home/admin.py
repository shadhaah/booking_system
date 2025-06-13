from django.contrib import admin

from .models import Departments,Doctors,Booking
# Register your models here.

admin.site.register(Departments)
admin.site.register(Doctors)

class BookingAdmin(admin.ModelAdmin):
    list_display= ('id','p_name','p_phone','p_email','doc_name','booking_date','booked_on')
    search_fields = ('p_name', 'p_phone', 'p_email', 'doc_name__doc_name')
    list_filter = ('doc_name', 'booking_date')


admin.site.register(Booking,BookingAdmin)