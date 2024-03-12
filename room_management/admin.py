from django.contrib import admin
from .models import Building, Fee, RoomType, Room, Customer

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
    list_display = ('alias', 'room', 'check_in_date', 'check_out_date', 'created_at', 'updated_at', 'is_active')
    list_filter = ('alias', 'room', 'check_in_date', 'check_out_date', 'created_at', 'updated_at', 'is_active')
    search_fields = ('alias', 'room', 'check_in_date', 'check_out_date', 'created_at', 'updated_at', 'is_active')
    ordering = ('alias', 'room', 'check_in_date', 'check_out_date', 'created_at', 'updated_at', 'is_active')