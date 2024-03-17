from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from core.decorators import staff_required

import json
import uuid

@staff_required
@login_required
def manage_rooms(request):
    rooms = Room.objects.filter(is_active=True).order_by('-room_number')
    room_types = RoomType.objects.filter(is_active=True)
    buildings = Building.objects.filter(is_active=True)

    breadcrumbs = [
        ('Dashboard', '/dashboard/'),
        ('Manage Rooms', None), 
    ]

    context = {
        'rooms': rooms,
        'room_types': room_types,
        'buildings': buildings,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'manage/rooms.html', context)

@staff_required
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

@staff_required
@login_required
def get_room_type_prices(request):
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    if not request.GET.get('room_type_id'):
        return JsonResponse({'success': False, 'message': 'Invalid room type id'})

    room_type_id = request.GET.get('room_type_id')
    room_type = RoomType.objects.filter(is_active=True, id=room_type_id).first()
    prices = room_type.fee.all().order_by('hours')
    data = []
    for price in prices:
        data.append({
            'id': price.id,
            'amount': price.amount,
            'hours': price.hours
        })
    return JsonResponse({'success': True, 'data': data})

@staff_required
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

@staff_required
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

@staff_required
@login_required
def manage_fee(request):
    fees = Fee.objects.filter(is_active=True).order_by('-created_at')

    breadcrumbs = [
        ('Dashboard', '/dashboard/'),
        ('Manage Fees', None), 
    ]

    context = {
        'fees': fees,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'manage/fees.html', context)

@staff_required
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

@staff_required
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

@staff_required
@login_required
def delete_fee(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    data = json.loads(request.body)
    fee_id = data.get('id')

    if not fee_id:
        return JsonResponse({'success': False, 'message': 'Invalid fee id'})

    fee = Fee.objects.filter(is_active=True, id=fee_id).first()
    fee.is_active = False
    fee.save()
    return JsonResponse({'success': True, 'message': 'Fee deleted successfuly'})

@staff_required
@login_required
def manage_room_types(request):
    room_types = RoomType.objects.filter(is_active=True).order_by('-created_at')

    for room_type in room_types:
        room_type.fee_ids = [fee.id for fee in room_type.fee.all()]

    fees = Fee.objects.filter(is_active=True)

    breadcrumbs = [
        ('Dashboard', '/dashboard/'),
        ('Manage Room Types', None), 
    ]
    
    context = {
        'room_types': room_types,
        'fees': fees,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'manage/room_types.html', context)

@staff_required
@login_required
def add_room_type(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    name = request.POST.get('room-type')
    fee_ids = request.POST.getlist('fees[]')

    if not name:
        return JsonResponse({'success': False, 'message': 'Name is required'})
    
    if not fee_ids:
        return JsonResponse({'success': False, 'message': 'At least one fee is required'})

   
    room_type = RoomType(name=name)
    room_type.save()

    for fee_id in fee_ids:
        fee = Fee.objects.get(id=fee_id)
        room_type.fee.add(fee)

    data = {
        'id': room_type.id,
        'name': room_type.name,
        'fees': [
            {
                'amount': fee.get_amount(),
                'hours': fee.get_hours(),
            }
            for fee in room_type.fee.all()
        ],
    }

    unformatted_data = {
        'id': room_type.id,
        'name': room_type.name,
        'fees': fee_ids,
    }
    
    return JsonResponse({'success': True, 'message': 'Room type added successfuly', 'data': data, 'unformatted_data': unformatted_data})

@staff_required
@login_required
def update_room_type(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    room_type_id = request.POST.get('room-type-id')
    name = request.POST.get('room-type')
    fee_ids = request.POST.getlist('fees[]')

    if not room_type_id:
        return JsonResponse({'success': False, 'message': 'Invalid room type id'})

    if not name:
        return JsonResponse({'success': False, 'message': 'Name is required'})
    
    if not fee_ids:
        return JsonResponse({'success': False, 'message': 'At least one fee is required'})

    room_type = RoomType.objects.get(id=room_type_id)

    if room_type.name == name and [fee.id for fee in room_type.fee.all()] == [int(fee_id) for fee_id in fee_ids]:
        return JsonResponse({'success': False, 'message': 'No changes made'})

    room_type.name = name
    room_type.fee.clear()
    room_type.save()

    for fee_id in fee_ids:
        fee = Fee.objects.get(id=fee_id)
        room_type.fee.add(fee)

    data = {
        'id': room_type.id,
        'name': room_type.name,
        'fees': [
            {
                'amount': fee.get_amount(),
                'hours': fee.get_hours(),
            }
            for fee in room_type.fee.all()
        ],
    }

    unformatted_data = {
        'id': room_type.id,
        'name': room_type.name,
        'fees': fee_ids,
    }
    
    return JsonResponse({'success': True, 'message': 'Room type updated successfuly', 'data': data, 'unformatted_data': unformatted_data})

@staff_required
@login_required
def delete_room_type(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    data = json.loads(request.body)
    room_type_id = data.get('id')

    if not room_type_id:
        return JsonResponse({'success': False, 'message': 'Invalid room type id'})

    room_type = RoomType.objects.filter(id=room_type_id).first()
    room_type.is_active = False
    room_type.save()
    return JsonResponse({'success': True, 'message': 'Room type deleted successfuly'})

@staff_required
@login_required
def manage_buildings(request):
    buildings = Building.objects.filter(is_active=True).order_by('-created_at')

    breadcrumbs = [
        ('Dashboard', '/dashboard/'),
        ('Manage Buildings', None), 
    ]

    context = {
        'buildings': buildings,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'manage/buildings.html', context)

@staff_required
@login_required
def add_building(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    name = request.POST.get('building-name')

    if not name:
        return JsonResponse({'success': False, 'message': 'Name is required'})

    building = Building(name=name)
    building.save()

    data = {
        'id': building.id,
        'name': building.name,
    }

    return JsonResponse({'success': True, 'message': 'Building added successfuly', 'data': data})

@staff_required
@login_required
def update_building(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    building_id = request.POST.get('building-id')
    name = request.POST.get('building-name')

    if not building_id:
        return JsonResponse({'success': False, 'message': 'Invalid building id'})

    if not name:
        return JsonResponse({'success': False, 'message': 'Name is required'})

    building = Building.objects.get(id=building_id)

    if building.name == name:
        return JsonResponse({'success': False, 'message': 'No changes made'})

    building.name = name
    building.save()

    data = {
        'id': building.id,
        'name': building.name,
    }
    
    return JsonResponse({'success': True, 'message': 'Building updated successfuly', 'data': data})

@staff_required
@login_required
def delete_building(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    data = json.loads(request.body)
    building_id = data.get('id')

    if not building_id:
        return JsonResponse({'success': False, 'message': 'Invalid building id'})

    building = Building.objects.filter(id=building_id).first()
    building.is_active = False
    building.save()
    
    return JsonResponse({'success': True, 'message': 'Building deleted successfuly'})

@login_required
def customer_check_in(request):
    rooms = Room.objects.filter(is_active=True).order_by('room_number')
    buildings = Building.objects.filter(is_active=True)
    customers = Customer.objects.filter(is_active=True).order_by('room__room_number')

    for customer in customers:
        customer.slug = uuid.uuid4().hex
        customer.save()

    breadcrumbs = [
        ('Dashboard', '/dashboard/'),
        ('Customer Check In', None), 
    ]

    context = {
        'rooms': rooms,
        'buildings': buildings,
        'breadcrumbs': breadcrumbs,
        'customers': customers
    }
    return render(request, 'check-in/check-in.html', context)

@login_required
def customer_check_out(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    data = json.loads(request.body)
    checkin_id = data.get('id')

    if not checkin_id:
        return JsonResponse({'success': False, 'message': 'Invalid check in id'})

    checkin = Customer.objects.filter(id=checkin_id).first()
    checkin.check_out_date = timezone.now()
    checkin.is_active = False
    checkin.save()

    data = {
        'id': checkin.id,
        'building_id': checkin.room.building.id,
        'building_active_count': checkin.room.building.get_active_room_count_number(),
        'building_active_count_text': checkin.room.building.get_active_room_count(),
        'room_id': checkin.room.id,
        'room_type_id': checkin.room.room_type.id,
        'room_get_room_for_dropdown': checkin.room.get_room_for_dropdown(),
    }

    return JsonResponse({'success': True, 'message': 'Customer checked out successfuly', 'data': data})

@login_required
def add_customer_check_in(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    room = request.POST.get('select-room')
    hours = request.POST.get('select-hours')
    amount_paid = request.POST.get('amount-paid')
    plate_number = request.POST.get('plate-number')
    extra_bed = request.POST.get('extra-bed')

    if not room or not hours or not amount_paid:
        return JsonResponse({'success': False, 'message': 'Room, hours and amount paid are required'})

    room = Room.objects.get(id=room)
    hours = Fee.objects.get(id=hours)

    customer = Customer(room=room, fee=hours, amount_paid=amount_paid, plate_number=plate_number, extra_bed=extra_bed)
    customer.save()

    customer.check_out_date = customer.check_in_date + timezone.timedelta(hours=hours.hours)
    customer.save()

    data = {
        'id': customer.id,
        'building_id': customer.room.building.id,
        'building_active_count': customer.room.building.get_active_room_count(),
        'room_id': customer.room.id,
        'room_number': customer.room.room_number,
        'room_name': str(customer.room.get_room()),
        'room_hours': str(customer.fee.get_hours()),
        'remaining_time': customer.get_remaining_time(),
        'unformatted_get_remaining_time': customer.unformatted_get_remaining_time(),
        'expected_check_out_date': str(customer.get_formatted_check_out_date()),
        'formatted_check_in_date': str(customer.get_formatted_check_in_date()),
        'formatted_check_out_date': str(customer.get_formatted_check_out_date()),
        'slug': customer.slug,
    }

    return JsonResponse({'success': True, 'message': 'Customer checked in successfuly', 'data': data})

@login_required
def view_check_in_summary(request, customer_slug):
    customer = Customer.objects.filter(slug=customer_slug).first()

    if not customer or not customer.is_active:
        return redirect('customer-check-in')

    total_price = customer.get_extra_bed_price_unformatted() + customer.get_room_price_unformatted()
    total_quantity = customer.extra_bed + 1

    customer.total_price = f"₱&nbsp;{total_price:,.2f}"
    customer.total_quantity = total_quantity
    customer.grand_total =  f"₱&nbsp;{(total_price - customer.amount_paid):,.2f}"
    customer.grand_total_unformatted = total_price - customer.amount_paid

    breadcrumbs = [
        ('Dashboard', '/dashboard/'),
        ('Customer Check In', '/customer/check-in/'),
        (f'{customer.room} Summary', None), 
    ]

    context = {
        'customer': customer,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'check-in/view-check-in-summary.html', context)