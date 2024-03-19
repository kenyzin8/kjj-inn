from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.store, name='store'),
    path('store/fetch-product/', views.fetch_product, name='fetch-product'),
    path('store/submit-purchase/', views.submit_purchase, name='submit-purchase'),
    path('inventory/product-types/', views.manage_product_types, name='product-types'),
    path('inventory/product-types/add/', views.add_product_type, name='add-product-type'),
    path('inventory/product-types/update/', views.update_product_type, name='update-product-type'),
    path('inventory/product-types/delete/', views.delete_product_type, name='delete-product-type'),
    path('inventory/products/', views.manage_products, name='products'),
    path('inventory/products/add/', views.add_product, name='add-product'),
    path('inventory/products/update/', views.update_product, name='update-product'),
    path('inventory/products/delete/', views.delete_product, name='delete-product'),
    path('inventory/barcodes/', views.manage_barcodes, name='barcodes'),
    path('inventory/barcodes/add/', views.add_barcode, name='add-barcode'),
]