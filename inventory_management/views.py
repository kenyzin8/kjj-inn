from django.shortcuts import render
from .models import *
from room_management.models import Room

def store(request):
    products = Product.objects.all()
    stocks = Stock.objects.all()
    active_rooms = Room.objects.filter(is_active=True)

    context = {
        'products': products,
        'stocks': stocks,
        'active_rooms': active_rooms
    }

    return render(request, 'store.html', context)