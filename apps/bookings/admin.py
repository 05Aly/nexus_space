from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import AddonService, Booking

@admin.register(AddonService)
class AddonServiceAdmin(ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_editable = ('price', 'is_active')

@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = ('reference_code', 'user', 'space', 'booking_date', 'start_hour', 'end_hour', 'total_price', 'status')
    list_filter = ('status', 'booking_date', 'space')
    list_editable = ('status',)
    search_fields = ('reference_code', 'user__username', 'space__name')
