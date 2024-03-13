from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
# login required
from django.contrib.auth.decorators import login_required

@login_required
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

@login_required
def add_room(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    room_number = request.POST.get('room-number')
    building_id = request.POST.get('building')
    room_type_id = request.POST.get('room-type')
    good_for = request.POST.get('good-for')

    if not room_number or not building_id or not room_type_id or not good_for:
        return JsonResponse({'success': False, 'message': 'Room number, building, room type and good for are required'})

    if int(room_number) < 0:
        return JsonResponse({'success': False, 'message': 'Invalid room number'})

    if int(good_for) < 1:
        return JsonResponse({'success': False, 'message': 'Invalid good for'})

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
            'date_updated': str(room.get_updated_at()),
            'index': Room.objects.filter(is_active=True).count()
        }

        unformatted_data = {
            'id': room.id,
            'room_number': room.room_number,
            'building': room.building.id,
            'room_type': room.room_type.id,
            'good_for': room.good_for,
        }
        
        return JsonResponse({'success': True, 'data': data, 'unformatted_data': unformatted_data, 'message': 'Room added successfuly'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
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

@login_required
def delete_room(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    data = json.loads(request.body)
    room_id = data.get('room_id')

    if not room_id:
        return JsonResponse({'success': False, 'message': 'Invalid room id'})

    room = Room.objects.filter(is_active=True, id=room_id).first()
    room.is_active = False
    room.save()
    return JsonResponse({'success': True})

@login_required
def update_room(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    room_id = request.POST.get('room-id')
    room_number = request.POST.get('room-number')
    building_id = request.POST.get('building')
    room_type_id = request.POST.get('room-type')
    good_for = request.POST.get('good-for')

    if not room_id:
        return JsonResponse({'success': False, 'message': 'Invalid room id'})
    
    if not room_number or not building_id or not room_type_id or not good_for:
        return JsonResponse({'success': False, 'message': 'Room number, building, room type and good for are required'})

    if int(room_number) < 0:
        return JsonResponse({'success': False, 'message': 'Invalid room number'})

    if int(good_for) < 1:
        return JsonResponse({'success': False, 'message': 'Invalid good for'})

    try:
        building = Building.objects.get(id=building_id)
        room_type = RoomType.objects.get(id=room_type_id)
        room = Room.objects.get(id=room_id)

        if room.room_number == int(room_number) and room.building == building and room.room_type == room_type and room.good_for == int(good_for):
            return JsonResponse({'success': False, 'message': 'No changes made'})

        room.room_number = room_number
        room.building = building
        room.room_type = room_type
        room.good_for = good_for
        room.save()

        data = {
            'id': room.id,
            'room_number': str(room.get_room()),
            'building': str(room.building.get_building()),
            'room_type': room.room_type.name,
            'good_for': str(room.get_good_for()),
            'date_updated': str(room.get_updated_at()),
        }

        unformatted_data = {
            'id': room.id,
            'room_number': room.room_number,
            'building': room.building.id,
            'room_type': room.room_type.id,
            'good_for': room.good_for,
        }
        
        return JsonResponse({'success': True, 'message': 'Room updated successfuly', 'data': data, 'unformatted_data': unformatted_data})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def manage_fee(request):
    fees = Fee.objects.filter(is_active=True).order_by('-created_at')
    context = {
        'fees': fees
    }
    return render(request, 'manage/fees.html', context)

@login_required
def add_fee(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    fee = float(request.POST.get('fee'))
    hours = int(request.POST.get('hours'))

    if not fee or not hours:
        return JsonResponse({'success': False, 'message': 'Fee and hours are required'})

    if fee <= 0:
        return JsonResponse({'success': False, 'message': 'Invalid fee amount'})
    
    if hours <= 0:
        return JsonResponse({'success': False, 'message': 'Invalid hours'})

    try:
        fee = Fee(amount=fee, hours=hours)
        fee.save()

        data = {
            'id': fee.id,
            'amount': fee.get_amount(),
            'hours': fee.get_hours(),
            'date_updated': str(fee.get_updated_at()),
        }

        unfomatted_data = {
            'id': fee.id,
            'amount': fee.amount,
            'hours': fee.hours,
        }
        
        return JsonResponse({'success': True, 'message': 'Fee added successfuly', 'data': data, 'unformatted_data': unfomatted_data})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def update_fee(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    fee_id = request.POST.get('fee-id')
    _fee = request.POST.get('fee')
    hours = request.POST.get('hours')

    if not fee_id:
        return JsonResponse({'success': False, 'message': 'Invalid fee id'})
    
    if not _fee or not hours:
        return JsonResponse({'success': False, 'message': 'Fee and hours are required'})

    if float(_fee) <= 0:
        return JsonResponse({'success': False, 'message': 'Invalid fee amount'})

    if int(hours) <= 0:
        return JsonResponse({'success': False, 'message': 'Invalid hours'})

    try:
        fee = Fee.objects.get(id=fee_id)
        if fee.amount == float(_fee) and fee.hours == int(hours):
            return JsonResponse({'success': False, 'message': 'No changes made'})

        fee.amount = float(_fee)
        fee.hours = int(hours)
        fee.save()

        data = {
            'id': fee.id,
            'amount': fee.get_amount(),
            'hours': fee.get_hours(),
            'date_updated': str(fee.get_updated_at()),
        }

        unformatted_data = {
            'id': fee.id,
            'amount': fee.amount,
            'hours': fee.hours,
        }
        
        return JsonResponse({'success': True, 'message': 'Fee updated successfuly', 'data': data, 'unformatted_data': unformatted_data})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})