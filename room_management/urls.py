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
   path('manage/room-types/update/', views.update_room_type, name='update-room-type'),
   path('manage/room-types/delete/', views.delete_room_type, name='delete-room-type'),
   path('manage/buildings/', views.manage_buildings, name='manage-buildings'),
   path('manage/buildings/add/', views.add_building, name='add-building'),
   path('manage/buildings/update/', views.update_building, name='update-building'),
   path('manage/buildings/delete/', views.delete_building, name='delete-building'),
   path('manage/extra-bed/', views.manage_extra_bed, name='manage-extra-bed'),
   path('manage/extra-bed/update/', views.update_extra_bed, name='update-extra-bed'),
   path('customer/check-in/', views.customer_check_in, name='customer-check-in'),
   path('customer/check-out/', views.customer_check_out, name='customer-check-out'),
   path('customer/check-in/add/', views.add_customer_check_in, name='add-customer-check-in'),
   path('customer/check-in/<str:customer_slug>/summary/', views.view_check_in_summary, name='view-check-in-summary'),
   path('customer/check-in/update-amount-paid/', views.update_amount_paid, name='update-amount-paid'),
]