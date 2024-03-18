from django.urls import path
from . import views

urlpatterns = [
    path('store/', views.store, name='store'),
    path('store/fetch-product/', views.fetch_product, name='fetch-product'),
    path('store/submit-purchase/', views.submit_purchase, name='submit-purchase'),
]