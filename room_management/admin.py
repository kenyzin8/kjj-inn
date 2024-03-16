from django.contrib import admin
from .models import Building, Fee, RoomType, Room, Customer, ExtraBedPrice

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'is_active')
    list_filter = ('name', 'created_at', 'updated_at', 'is_active')
    search_fields = ('name', 'created_at', 'updated_at', 'is_active')
    ordering = ('name', 'created_at', 'updated_at', 'is_active')

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'hours', 'created_at', 'updated_at', 'is_active')
    list_filter = ('amount', 'hours', 'created_at', 'updated_at', 'is_active')
    search_fields = ('amount', 'hours', 'created_at', 'updated_at', 'is_active')
    ordering = ('amount', 'hours', 'created_at', 'updated_at', 'is_active')

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'is_active')
    list_filter = ('name', 'created_at', 'updated_at', 'is_active')
    search_fields = ('name', 'created_at', 'updated_at', 'is_active')
    ordering = ('name', 'created_at', 'updated_at', 'is_active')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'building', 'room_type', 'good_for', 'created_at', 'updated_at', 'is_active')
    list_filter = ('room_number', 'building', 'room_type', 'good_for', 'created_at', 'updated_at', 'is_active')
    search_fields = ('room_number', 'building', 'room_type', 'good_for', 'created_at', 'updated_at', 'is_active')
    ordering = ('room_number', 'building', 'room_type', 'good_for', 'created_at', 'updated_at', 'is_active')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('alias', 'room', 'check_in_date', 'check_out_date', 'updated_at', 'amount_paid', 'plate_number', 'extra_bed', 'is_active')
    list_filter = ('alias', 'room', 'check_in_date', 'check_out_date', 'updated_at', 'amount_paid', 'plate_number', 'extra_bed', 'is_active')
    search_fields = ('alias', 'room', 'check_in_date', 'check_out_date', 'updated_at', 'amount_paid', 'plate_number', 'extra_bed', 'is_active')
    ordering = ('alias', 'room', 'check_in_date', 'check_out_date', 'updated_at', 'amount_paid', 'plate_number', 'extra_bed', 'is_active')

@admin.register(ExtraBedPrice)
class ExtraBedPriceAdmin(admin.ModelAdmin):
    list_display = ('price', 'created_at', 'updated_at', 'is_active')
    list_filter = ('price', 'created_at', 'updated_at', 'is_active')
    search_fields = ('price',)
    ordering = ('price', 'created_at', 'updated_at', 'is_active')

    def has_add_permission(self, request, obj=None):
        return not ExtraBedPrice.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
