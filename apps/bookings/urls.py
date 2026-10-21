from django.urls import path
from . import views

urlpatterns = [
    path('check-availability/<int:space_id>/', views.check_availability_htmx, name='check_availability'),
    path('create/<int:space_id>/', views.create_booking_view, name='create_booking'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking_view, name='cancel_booking'),
]
