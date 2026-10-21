from django.db import models

class Amenity(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم التجهيز / الخدمة")
    icon_name = models.CharField(
        max_length=50,
        default="check",
        verbose_name="كود أيقونة Lucide",
        help_text="مثال: wifi, monitor, coffee, wind, shield-check, mic"
    )

    class Meta:
        verbose_name = "تجهيز / مرفق"
        verbose_name_plural = "التجهيزات والمرافق"

    def __str__(self):
        return self.name

class SpaceCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم التصنيف")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "تصنيف وحدة"
        verbose_name_plural = "تصنيفات الوحدات"

    def __str__(self):
        return self.name

class Space(models.Model):
    name = models.CharField(max_length=150, verbose_name="اسم الوحدة / القاعة")
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(SpaceCategory, on_delete=models.CASCADE, related_name='spaces', verbose_name="التصنيف")
    floor_level = models.CharField(max_length=50, default="الطابق الأول", verbose_name="الطابق / الموقع")
    area_sqm = models.PositiveIntegerField(default=28, verbose_name="المساحة (م²)")
    capacity = models.PositiveIntegerField(verbose_name="السعة (عدد الأشخاص)")
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=0, verbose_name="السعر لكل ساعة (جنيه)")
    description = models.TextField(verbose_name="الوصف والتفاصيل")
    image_url = models.URLField(
        default="https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=1000&q=80",
        verbose_name="رابط صورة الوحدة"
    )
    amenities = models.ManyToManyField(Amenity, blank=True, verbose_name="التجهيزات المتوفرة")
    is_available = models.BooleanField(default=True, verbose_name="متاحة للحجز؟")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتيب العرض")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "وحدة / مساحة"
        verbose_name_plural = "الوحدات والمساحات"

    def __str__(self):
        return f"{self.name} ({self.price_per_hour} جنيه / ساعة)"
