# NexusSpace | منصة إدارة وحجز مساحات العمل والقاعات

نظام ويب متكامل لإدارة وحجز المكاتب وقاعات الاجتماعات والتدريب مبني باستخدام Django و HTMX و Tailwind CSS مع لوحة تحكم Unfold.

## خطوات التشغيل السريع

1. إنشاء وتفعيل البيئة الافتراضية:
   python -m venv venv
   venv\Scripts\activate

2. تثبيت المكتبات:
   pip install -r requirements.txt

3. تهيئة قاعدة البيانات والبيانات الأساسية:
   python manage.py makemigrations cms spaces bookings
   python manage.py migrate
   python manage.py seed_data

4. تشغيل السيرفر:
   python manage.py runserver

## بيانات الدخول التجريبية
- مدير النظام (Admin): admin / admin123
- عميل (Client): client / client123
