from django.contrib import admin
from .models import *

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'is_active')
    list_filter = ('name', 'created_at', 'updated_at', 'is_active')
    search_fields = ('name', 'created_at', 'updated_at', 'is_active')
    ordering = ('name', 'created_at', 'updated_at', 'is_active')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'created_at', 'updated_at', 'is_active')
    list_filter = ('name', 'product_type', 'created_at', 'updated_at', 'is_active')
    search_fields = ('name', 'product_type', 'created_at', 'updated_at', 'is_active')
    ordering = ('name', 'product_type', 'created_at', 'updated_at', 'is_active')

@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'product', 'created_at', 'updated_at', 'is_active')
    list_filter = ('barcode', 'product', 'created_at', 'updated_at', 'is_active')
    search_fields = ('barcode', 'product', 'created_at', 'updated_at', 'is_active')
    ordering = ('barcode', 'product', 'created_at', 'updated_at', 'is_active')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'price', 'batch_no', 'expiry_date', 'created_at', 'updated_at', 'is_active')
    list_filter = ('product', 'quantity', 'price', 'batch_no', 'expiry_date', 'created_at', 'updated_at', 'is_active')
    search_fields = ('product', 'quantity', 'price', 'batch_no', 'expiry_date', 'created_at', 'updated_at', 'is_active')
    ordering = ('product', 'quantity', 'price', 'batch_no', 'expiry_date', 'created_at', 'updated_at', 'is_active')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at', 'is_active')
    list_filter = ('created_at', 'updated_at', 'is_active')
    search_fields = ('created_at', 'updated_at', 'is_active')
    ordering = ('created_at', 'updated_at', 'is_active')

@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'stock', 'quantity', 'created_at', 'updated_at', 'is_active')
    list_filter = ('purchase', 'stock', 'quantity', 'created_at', 'updated_at', 'is_active')
    search_fields = ('purchase', 'stock', 'quantity', 'created_at', 'updated_at', 'is_active')
    ordering = ('purchase', 'stock', 'quantity', 'created_at', 'updated_at', 'is_active')