from django.urls import path
from . import views

urlpatterns = [
   path('manage/rooms/', views.manage_rooms, name='manage-rooms'),
   path('manage/rooms/add/', views.add_room, name='add-room'),
   path('manage/rooms/add/get-room-type-prices/', views.get_room_type_prices, name='get-room-type-prices'),
   path('manage/rooms/delete/', views.delete_room, name='delete-room'),
]