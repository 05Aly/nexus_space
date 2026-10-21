from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import SiteConfiguration, FAQ

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(ModelAdmin):
    def has_add_permission(self, request):
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)
