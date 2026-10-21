import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from apps.spaces.models import Space

class AddonService(models.Model):
    name = models.CharField(max_length=100, verbose_name="الخدمة الإضافية")
    price = models.DecimalField(max_digits=6, decimal_places=0, verbose_name="السعر (جنيه)")
    is_active = models.BooleanField(default=True, verbose_name="متاحة؟")

    class Meta:
        verbose_name = "خدمة إضافية"
        verbose_name_plural = "الخدمات الإضافية"

    def __str__(self):
        return f"{self.name} (+{self.price} جنيه)"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'قيد المراجعة'),
        ('CONFIRMED', 'مؤكد'),
        ('CANCELLED', 'ملغي'),
    ]

    reference_code = models.CharField(max_length=12, unique=True, editable=False, verbose_name="كود الحجز")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name="العميل")
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='bookings', verbose_name="الوحدة")
    booking_date = models.DateField(verbose_name="تاريخ الحجز")
    start_hour = models.PositiveSmallIntegerField(verbose_name="ساعة البدء (24h)")
    end_hour = models.PositiveSmallIntegerField(verbose_name="ساعة الانتهاء (24h)")
    addons = models.ManyToManyField(AddonService, blank=True, verbose_name="الخدمات الإضافية")
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="الإجمالي (جنيه)")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='CONFIRMED', verbose_name="الحالة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        ordering = ['-booking_date', '-start_hour']
        verbose_name = "حجز"
        verbose_name_plural = "سجل الحجوزات"

    def __str__(self):
        return f"{self.reference_code} | {self.space.name} ({self.booking_date})"

    def clean(self):
        if self.start_hour is not None and self.end_hour is not None:
            if self.start_hour >= self.end_hour:
                raise ValidationError("ساعة الانتهاء يجب أن تكون بعد ساعة البدء.")
            if self.start_hour < 8 or self.end_hour > 23:
                raise ValidationError("مواعيد العمل المتاحة من الساعة 08:00 وحتى 23:00.")

            overlapping = Booking.objects.filter(
                space=self.space,
                booking_date=self.booking_date,
                status__in=['PENDING', 'CONFIRMED']
            ).exclude(pk=self.pk).filter(
                Q(start_hour__lt=self.end_hour) & Q(end_hour__gt=self.start_hour)
            )
            if overlapping.exists():
                raise ValidationError("هذه الوحدة محجوزة بالفعل في الفترة الزمنية المختارة.")

    def save(self, *args, **kwargs):
        if not self.reference_code:
            self.reference_code = "NX-" + uuid.uuid4().hex[:6].upper()
        hours = Decimal(max(1, self.end_hour - self.start_hour))
        self.total_price = hours * self.space.price_per_hour
        super().save(*args, **kwargs)
