from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookings/', include('apps.bookings.urls')),
    path('api/index', include('apps.spaces.urls')),
    path('', include('apps.spaces.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
