from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from apps.spaces.models import Space
from .models import Booking, AddonService

def check_availability_htmx(request, space_id):
    space = get_object_or_404(Space, id=space_id)
    date_str = request.GET.get('booking_date')
    start_hour = int(request.GET.get('start_hour', 9))
    end_hour = int(request.GET.get('end_hour', 11))
    addon_ids = request.GET.getlist('addons')

    bookings_on_date = []
    if date_str:
        bookings_on_date = Booking.objects.filter(
            space=space,
            booking_date=date_str,
            status__in=['PENDING', 'CONFIRMED']
        )

    hours_count = max(0, end_hour - start_hour)
    base_cost = Decimal(hours_count) * space.price_per_hour
    addons_cost = sum(a.price for a in AddonService.objects.filter(id__in=addon_ids))
    total_cost = base_cost + addons_cost if hours_count > 0 else Decimal(0)

    has_conflict = False
    for b in bookings_on_date:
        if start_hour < b.end_hour and end_hour > b.start_hour:
            has_conflict = True
            break

    context = {
        'bookings_on_date': bookings_on_date,
        'hours_count': hours_count,
        'base_cost': base_cost,
        'addons_cost': addons_cost,
        'total_cost': total_cost,
        'has_conflict': has_conflict,
        'invalid_range': start_hour >= end_hour,
    }
    return render(request, 'bookings/partials/availability_box.html', context)

@login_required(login_url='/login/')
def create_booking_view(request, space_id):
    space = get_object_or_404(Space, id=space_id)
    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        start_hour = int(request.POST.get('start_hour', 9))
        end_hour = int(request.POST.get('end_hour', 11))
        addon_ids = request.POST.getlist('addons')

        booking = Booking(
            user=request.user,
            space=space,
            booking_date=booking_date,
            start_hour=start_hour,
            end_hour=end_hour,
        )
        try:
            booking.full_clean()
            booking.save()
            if addon_ids:
                addons = AddonService.objects.filter(id__in=addon_ids)
                booking.addons.set(addons)
                booking.total_price += sum(a.price for a in addons)
                booking.save()
            messages.success(request, f"تم تأكيد الحجز بنجاح. كود الحجز: {booking.reference_code}")
            return redirect('my_bookings')
        except ValidationError as e:
            for err in e.messages:
                messages.error(request, err)
            return redirect('space_detail', slug=space.slug)

    return redirect('space_detail', slug=space.slug)

@login_required(login_url='/login/')
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required(login_url='/login/')
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.status = 'CANCELLED'
    booking.save()
    messages.info(request, f"تم إلغاء الحجز رقم {booking.reference_code}.")
    return redirect('my_bookings')
