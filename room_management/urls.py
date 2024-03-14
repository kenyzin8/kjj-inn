from django.urls import path
from . import views

urlpatterns = [
   path('manage/rooms/', views.manage_rooms, name='manage-rooms'),
   path('manage/rooms/add/', views.add_room, name='add-room'),
   path('manage/rooms/add/get-room-type-prices/', views.get_room_type_prices, name='get-room-type-prices'),
   path('manage/rooms/delete/', views.delete_room, name='delete-room'),
   path('manage/rooms/update/', views.update_room, name='update-room'),
   path('manage/fees/', views.manage_fee, name='manage-fees'),
   path('manage/fees/add/', views.add_fee, name='add-fee'),
   path('manage/fees/update/', views.update_fee, name='update-fee'),
   path('manage/fees/delete/', views.delete_fee, name='delete-fee'),
   path('manage/room-types/', views.manage_room_types, name='manage-room-types'),
   path('manage/room-types/add/', views.add_room_type, name='add-room-type'),
]