from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json

def manage_rooms(request):
    rooms = Room.objects.filter(is_active=True).order_by('-room_number')
    room_types = RoomType.objects.filter(is_active=True)
    buildings = Building.objects.filter(is_active=True)
    context = {
        'rooms': rooms,
        'room_types': room_types,
        'buildings': buildings
    }
    return render(request, 'manage/rooms.html', context)

def add_room(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    room_number = request.POST.get('room-number')
    building_id = request.POST.get('building')
    room_type_id = request.POST.get('room-type')
    good_for = request.POST.get('good-for')

    try:
        building = Building.objects.get(id=building_id)
        room_type = RoomType.objects.get(id=room_type_id)
        room = Room(room_number=room_number, building=building, room_type=room_type, good_for=good_for)
        room.save()

        data = {
            'id': room.id,
            'room_number': str(room.get_room()),
            'building': str(room.building.get_building()),
            'room_type': room.room_type.name,
            'good_for': str(room.get_good_for()),
            'index': Room.objects.filter(is_active=True).count()
        }
        
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

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

def delete_room(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    data = json.loads(request.body)
    room_id = data.get('room_id')

    print(request.POST.get('room_id'))

    if not room_id:
        return JsonResponse({'success': False, 'message': 'Invalid room id'})

    room = Room.objects.filter(is_active=True, id=room_id).first()
    room.is_active = False
    room.save()
    return JsonResponse({'success': True})