from django.db import models

class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100, default="NexusSpace", verbose_name="اسم المنصة")
    hero_title_line1 = models.CharField(max_length=150, default="مساحات عمل وقاعات", verbose_name="عنوان الواجهة (السطر الأول)")
    hero_title_line2 = models.CharField(max_length=150, default="بكل احترافية في مكان واحد", verbose_name="عنوان الواجهة (السطر الثاني)")
    hero_subtitle = models.TextField(
        default="احجز مساحتك المثالية للعمل أو عقد الاجتماعات أو تنظيم الفعاليات من خلال منصة NexusSpace، بكل سهولة ومرونة.",
        verbose_name="الوصف المختصر في الواجهة"
    )
    hero_image_url = models.URLField(
        default="https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=1400&q=85",
        verbose_name="صورة الواجهة الرئيسية (Hero)"
    )
    cta_banner_title = models.CharField(max_length=150, default="مساحتك المثالية بانتظارك", verbose_name="عنوان اللوحة الداكنة")
    cta_banner_subtitle = models.TextField(
        default="سواء كنت تعمل بمفردك أو مع فريقك، نحن نوفر لك المكان المناسب.",
        verbose_name="وصف اللوحة الداكنة"
    )
    contact_email = models.EmailField(default="info@nexusspace.com", verbose_name="البريد الإلكتروني")
    phone_number = models.CharField(max_length=30, default="+20 2 2519 0000", verbose_name="رقم الهاتف")
    address = models.CharField(max_length=250, default="شارع 9، المعادي، القاهرة", verbose_name="العنوان الفعلي")
    working_hours = models.CharField(max_length=100, default="يومياً من 08:00 صباحاً إلى 11:00 مساءً", verbose_name="ساعات العمل")

    class Meta:
        verbose_name = "إعدادات المنصة الأساسية"
        verbose_name_plural = "إعدادات المنصة الأساسية"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="السؤال")
    answer = models.TextField(verbose_name="الإجابة")
    order = models.PositiveIntegerField(default=0, verbose_name="الترتيب")

    class Meta:
        ordering = ['order']
        verbose_name = "سؤال شائع"
        verbose_name_plural = "الأسئلة الشائعة"

    def __str__(self):
        return self.question
