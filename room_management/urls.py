from django.urls import path
from . import views

urlpatterns = [
   path('manage/rooms/', views.manage_rooms, name='manage-rooms')
]