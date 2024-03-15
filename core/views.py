from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import LoginForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.decorators import staff_required
from django.utils import timezone
import json

def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    user = request.user

    context = {
        'user': user
    }

    return render(request, 'admin/dashboard.html', context)

@login_required
def logout_user(request):
    logout(request)
    return redirect('login') 

def login_user(request):
    if(request.user.is_authenticated):
        return redirect('admin-dashboard')

    error_message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('admin-dashboard') 
            else:
                error_message = 'Invalid username or password.'
    else:
        form = LoginForm() 

    return render(request, 'login.html', {'form': form, 'error_message': error_message})

@staff_required
@login_required
def user_management(request):
    users = User.objects.filter(is_active=True).order_by('-date_joined')
    context = {
        'users': users
    }
    return render(request, 'admin/users.html', context)

@staff_required
@login_required
def add_user(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    username = request.POST.get('username')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm-password')
    is_staff = request.POST.get('is-staff')

    if(is_staff == 'on'):
        is_staff = True
    else:
        is_staff = False

    if not firstname or not lastname or not username or not password or not confirm_password:
        return JsonResponse({'success': False, 'message': 'All fields are required'})

    if username in [user.username for user in User.objects.all()]:
        return JsonResponse({'success': False, 'message': 'Username already exists', 'username_exists': True})

    if password != confirm_password:
        return JsonResponse({'success': False, 'message': 'Passwords do not match', 'password_correct': False})

    user = User.objects.create_user(username=username, password=password, first_name=firstname, last_name=lastname, is_staff=is_staff)
    user.save()

    data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'is_staff': user.is_staff,
        'date_created': user.date_joined.strftime('%B %d, %Y - %I:%M %p'),
    }

    return JsonResponse({'success': True, 'message': 'User added successfully', 'data': data})

@staff_required
@login_required
def update_user(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    user_id = request.POST.get('user-id')
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    username = request.POST.get('username')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm-password')
    is_staff = request.POST.get('is-staff')

    if(is_staff == 'on'):
        is_staff = True
    else:
        is_staff = False
        
    if not user_id or not firstname or not lastname or not username:
        return JsonResponse({'success': False, 'message': 'All fields are required'})

    user = User.objects.get(id=user_id)

    if username in [user.username for user in User.objects.exclude(id=user_id)]:
        return JsonResponse({'success': False, 'message': 'Username already exists', 'username_exists': True})

    if password and confirm_password:
        if password != confirm_password:
            return JsonResponse({'success': False, 'message': 'Passwords do not match', 'password_correct': False})

    user.first_name = firstname
    user.last_name = lastname
    user.username = username
    if password:
        user.password = password
    user.is_staff = is_staff

    user.save()

    user.date_joined = timezone.localtime(user.date_joined)

    data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'is_staff': user.is_staff,
        'date_created': user.date_joined.strftime('%B %d, %Y - %I:%M %p'),
    }

    return JsonResponse({'success': True, 'message': 'User updated successfully', 'data': data})

@staff_required
@login_required
def delete_user(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    data = json.loads(request.body)
    user_id = data.get('id')

    if not user_id:
        return JsonResponse({'success': False, 'message': 'User ID is required'})

    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()

    return JsonResponse({'success': True, 'message': 'User deleted successfully'})