from django.urls import path
from . import views

urlpatterns = [
    path('reports/sales/', views.sales, name='sales'),
    path('reports/sales/<str:sale_slug>/', views.view_sales, name='view-sales')
]