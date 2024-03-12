from django.shortcuts import render
from django.http import JsonResponse
from .models import *

def manage_rooms(request):
    rooms = Room.objects.filter(is_active=True)
    room_types = RoomType.objects.filter(is_active=True)
    context = {
        'rooms': rooms,
        'room_types': room_types
    }
    return render(request, 'manage/rooms.html', context)

def add_room(request):
    if request.method != 'POST':
        return JsonResponse({'sucess': False, 'message': 'Invalid request method'})

def get_room_type_prices(request):

    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    if not request.GET.get('room_type_id'):
        return JsonResponse({'success': False, 'message': 'Invalid room type id'})

    room_type_id = request.GET.get('room_type_id')
    room_type = RoomType.objects.filter(is_active=True, id=room_type_id).first()
    prices = room_type.fee.all()
    data = []
    for price in prices:
        data.append({
            'id': price.id,
            'amount': price.amount,
            'hours': price.hours
        })
    return JsonResponse({'success': True, 'data': data})
    