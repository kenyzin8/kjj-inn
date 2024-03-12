from django.shortcuts import render
from .models import *
# Create your views here.

def manage_rooms(request):
    rooms = Room.objects.filter(is_active=True)
    context = {
        'rooms': rooms
    }
    return render(request, 'manage/rooms.html', context)