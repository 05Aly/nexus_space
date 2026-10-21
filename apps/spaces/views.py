from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Space, SpaceCategory, Amenity
from apps.cms.models import FAQ
from apps.bookings.models import AddonService

def home_view(request):
    category_slug = request.GET.get('category')
    spaces = Space.objects.filter(is_available=True)
    if category_slug:
        spaces = spaces.filter(category__slug=category_slug)

    context = {
        'spaces': spaces,
        'categories': SpaceCategory.objects.all(),
        'selected_category': category_slug,
        'faqs': FAQ.objects.all(),
        'addons': AddonService.objects.filter(is_active=True),
        'amenities': Amenity.objects.all(),
    }
    return render(request, 'spaces/home.html', context)

def space_detail_view(request, slug):
    space = get_object_or_404(Space, slug=slug, is_available=True)
    addons = AddonService.objects.filter(is_active=True)
    return render(request, 'spaces/space_detail.html', {'space': space, 'addons': addons})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "تم تسجيل الدخول بنجاح.")
            return redirect('home')
        else:
            messages.error(request, "بيانات الدخول غير صحيحة.")
    return render(request, 'spaces/auth.html', {'mode': 'login'})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email', '')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, "اسم المستخدم مسجل بالفعل.")
        elif username and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, "تم إنشاء الحساب وتسجيل الدخول بنجاح.")
            return redirect('home')
    return render(request, 'spaces/auth.html', {'mode': 'register'})

def demo_login_view(request, role):
    if role == 'admin':
        user = User.objects.filter(username='admin').first()
        if user:
            login(request, user)
            messages.success(request, "تم الدخول بصلاحيات مدير النظام. يمكنك تعديل الأسعار والوحدات والمحتوى من لوحة الإدارة.")
            return redirect('/admin/')
    else:
        user = User.objects.filter(username='client').first()
        if user:
            login(request, user)
            messages.success(request, "تم تسجيل الدخول بحساب العميل التجريبي.")
            return redirect('home')
    messages.error(request, "يرجى تشغيل أمر python manage.py seed_data أولاً.")
    return redirect('home')

def logout_view(request):
    logout(request)
    messages.info(request, "تم تسجيل الخروج.")
    return redirect('home')
