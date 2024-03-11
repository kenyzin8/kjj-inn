from django.shortcuts import render

# Create your views here.

def manage_rooms(request):
    return render(request, 'manage/rooms.html')