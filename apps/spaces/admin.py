from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Amenity, SpaceCategory, Space

@admin.register(Amenity)
class AmenityAdmin(ModelAdmin):
    list_display = ('name', 'icon_name')

@admin.register(SpaceCategory)
class SpaceCategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Space)
class SpaceAdmin(ModelAdmin):
    list_display = ('name', 'category', 'floor_level', 'area_sqm', 'capacity', 'price_per_hour', 'is_available', 'order')
    list_filter = ('category', 'is_available')
    list_editable = ('price_per_hour', 'is_available', 'order')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
