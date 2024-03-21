from django.urls import path
from . import views

urlpatterns = [
    path('reports/sales/', views.sales, name='sales')
]