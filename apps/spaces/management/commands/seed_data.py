from datetime import date
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.cms.models import SiteConfiguration, FAQ
from apps.spaces.models import Amenity, SpaceCategory, Space
from apps.bookings.models import AddonService, Booking

class Command(BaseCommand):
    help = 'Seeds the database matching the reference design specification'

    def handle(self, *args, **kwargs):
        self.stdout.write("جاري تهيئة بيانات NexusSpace المطابقة للتصميم المرجعي...")

        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@nexusspace.com', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        client_user, created = User.objects.get_or_create(
            username='client',
            defaults={'email': 'client@nexusspace.com', 'first_name': 'علي', 'last_name': 'عماد'}
        )
        if created:
            client_user.set_password('client123')
            client_user.save()

        SiteConfiguration.objects.get_or_create(pk=1)

        amenities_data = [
            ("إنترنت فائق السرعة", "wifi"),
            ("شاشة عرض ذكية", "monitor"),
            ("نظام صوتي وميكروفون", "mic"),
            ("تكييف مركزي مستقل", "wind"),
            ("سبورة تخطيط", "presentation"),
            ("مشروبات وضيافة", "coffee"),
        ]
        amenities_objs = []
        for name, icon_name in amenities_data:
            obj, _ = Amenity.objects.update_or_create(name=name, defaults={'icon_name': icon_name})
            amenities_objs.append(obj)

        cat_meeting, _ = SpaceCategory.objects.update_or_create(
            slug='meeting-rooms',
            defaults={'name': 'قاعات اجتماعات'}
        )
        cat_coworking, _ = SpaceCategory.objects.update_or_create(
            slug='coworking-spaces',
            defaults={'name': 'مساحات عمل مشتركة'}
        )
        cat_training, _ = SpaceCategory.objects.update_or_create(
            slug='training-halls',
            defaults={'name': 'قاعات تدريب'}
        )

        # Reference cards matching design.md & screenshot
        spaces_data = [
            {
                'name': 'قاعة اجتماعات',
                'slug': 'meeting-room-a1',
                'category': cat_meeting,
                'floor_level': 'الطابق الأول',
                'area_sqm': 28,
                'capacity': 12,
                'price_per_hour': 150,
                'order': 1,
                'description': 'قاعة اجتماعات مجهزة بطاولة خشبية طويلة وكراسي مريحة وشاشة عرض جدارية مع نوافذ زجاجية وإضاءة طبيعية.',
                'image_url': 'https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=1000&q=80',
            },
            {
                'name': 'مكتب فريق',
                'slug': 'team-office-b1',
                'category': cat_coworking,
                'floor_level': 'الطابق الأول',
                'area_sqm': 18,
                'capacity': 6,
                'price_per_hour': 120,
                'order': 2,
                'description': 'مساحة عمل مشتركة ومكتب مخصص للفرق مزود بمكاتب حديثة وإضاءة طبيعية ونباتات داخلية لبيئة عمل هادئة.',
                'image_url': 'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1000&q=80',
            },
            {
                'name': 'قاعة تدريب',
                'slug': 'training-hall-c1',
                'category': cat_training,
                'floor_level': 'الطابق الثاني',
                'area_sqm': 60,
                'capacity': 40,
                'price_per_hour': 200,
                'order': 3,
                'description': 'قاعة تدريب واسعة مجهزة بصفوف كراسٍ منظمة وشاشة عرض كبيرة لورش العمل والدورات التدريبية.',
                'image_url': 'https://images.unsplash.com/photo-1517502884422-41eaead166d4?auto=format&fit=crop&w=1000&q=80',
            },
        ]

        created_spaces = []
        for s in spaces_data:
            space_obj, _ = Space.objects.update_or_create(slug=s['slug'], defaults=s)
            space_obj.amenities.set(amenities_objs)
            created_spaces.append(space_obj)

        AddonService.objects.update_or_create(name="ضيافة ومشروبات للاجتماع", defaults={'price': 80, 'is_active': True})
        AddonService.objects.update_or_create(name="جهاز عرض وتسجيل إضافي", defaults={'price': 100, 'is_active': True})
        AddonService.objects.update_or_create(name="دعم تقني مخصص", defaults={'price': 120, 'is_active': True})

        FAQ.objects.update_or_create(
            question="ما هي سياسة تعديل أو إلغاء الحجز المؤكد؟",
            defaults={'answer': 'يمكنك إلغاء الحجز من صفحة حجوزاتي بدون رسوم قبل موعد الحجز بـ 24 ساعة.', 'order': 1}
        )
        FAQ.objects.update_or_create(
            question="كيف يتم احتساب التكلفة الإجمالية؟",
            defaults={'answer': 'تحسب التكلفة بضرب عدد الساعات في سعر الساعة للوحدة مع إضافة أي خدمات إضافية مختارة.', 'order': 2}
        )
        FAQ.objects.update_or_create(
            question="هل يمكن حجز نفس القاعة من عميلين في نفس الوقت؟",
            defaults={'answer': 'لا، يتحقق النظام في الوقت الحقيقي ويمنع أي تقاطع زمني تلقائياً.', 'order': 3}
        )

        if created_spaces and not Booking.objects.exists():
            Booking.objects.create(
                user=client_user,
                space=created_spaces[0],
                booking_date=date.today(),
                start_hour=10,
                end_hour=12,
                status='CONFIRMED'
            )

        self.stdout.write(self.style.SUCCESS("تم تجهيز قاعدة البيانات بنجاح."))
