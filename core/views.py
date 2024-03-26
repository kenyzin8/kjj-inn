from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import LoginForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.decorators import staff_required
from django.utils import timezone

from inventory_management.models import Purchase, PurchaseItem
from room_management.models import Customer, ExtraBedPrice

from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth

import json
import datetime

def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    user = request.user
    current_date = timezone.now()
    current_month_start = current_date.replace(day=1)
    last_month_end = current_month_start - timezone.timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)
    two_months_ago_end = last_month_start - timezone.timedelta(days=1)
    two_months_ago_start = two_months_ago_end.replace(day=1)

    last_month_room_sales = 0
    last_month_customers = Customer.objects.filter(
        check_in_date__range=[last_month_start, last_month_end],
        is_active=False
    )

    for customer in last_month_customers:
        total_extra_items_subtotal = 0
        purchase = Purchase.objects.filter(customer=customer).first()
        if purchase:
            purchase_items = PurchaseItem.objects.filter(purchase=purchase)
            for item in purchase_items:
                total_extra_items_subtotal += item.price_at_purchase * item.quantity

        total_extra_bed_subtotal = customer.extra_bed * customer.extra_bed_price_at_check_in

        subtotal = customer.price_at_check_in + total_extra_items_subtotal + total_extra_bed_subtotal
        last_month_room_sales += subtotal

    last_month_walk_in_sales = PurchaseItem.objects.filter(
        purchase__created_at__range=[last_month_start, last_month_end],
        purchase__is_walk_in=True,
        is_active=True
    ).aggregate(total=Sum('price_at_purchase'))['total'] or 0

    previous_month_room_sales = 0
    previous_month_customers = Customer.objects.filter(
        check_in_date__range=[two_months_ago_start, two_months_ago_end],
        is_active=False
    )

    for customer in previous_month_customers:
        total_extra_items_subtotal = 0
        purchase = Purchase.objects.filter(customer=customer).first()
        if purchase:
            purchase_items = PurchaseItem.objects.filter(purchase=purchase)
            for item in purchase_items:
                total_extra_items_subtotal += item.price_at_purchase * item.quantity

        total_extra_bed_subtotal = customer.extra_bed * customer.extra_bed_price_at_check_in

        subtotal = customer.price_at_check_in + total_extra_items_subtotal + total_extra_bed_subtotal
        previous_month_room_sales += subtotal

    previous_month_walk_in_sales = PurchaseItem.objects.filter(
        purchase__created_at__range=[two_months_ago_start, two_months_ago_end],
        purchase__is_walk_in=True,
        is_active=True
    ).aggregate(total=Sum('price_at_purchase'))['total'] or 0

    last_month_total_sales = last_month_room_sales + last_month_walk_in_sales
    previous_month_total_sales = previous_month_room_sales + previous_month_walk_in_sales

    if previous_month_total_sales > 0:
        growth_percentage = ((last_month_total_sales - previous_month_total_sales) / previous_month_total_sales) * 100
    else:
        growth_percentage = 100 if last_month_total_sales > 0 else 0

    if growth_percentage > 0:
        growth_icon = 'fa-arrow-up'
        growth_color = 'text-green-500 dark:text-green-500'
    elif growth_percentage < 0:
        growth_icon = 'fa-arrow-down'
        growth_color = 'text-red-500 dark:text-red-500'
    else:
        growth_icon = 'fa-minus'
        growth_color = 'text-yellow-500 dark:text-yellow-500'

    last_month_customers = Customer.objects.filter(
        check_in_date__range=[last_month_start, last_month_end],
        is_active=False
    ).count() + Purchase.objects.filter(
        created_at__range=[last_month_start, last_month_end],
        is_walk_in=True,
        is_active=True
    ).count()

    previous_month_customers = Customer.objects.filter(
        check_in_date__range=[two_months_ago_start, two_months_ago_end],
        is_active=False
    ).count() + Purchase.objects.filter(
        created_at__range=[two_months_ago_start, two_months_ago_end],
        is_walk_in=True,
        is_active=True
    ).count()

    if previous_month_customers > 0:
        customer_growth_percentage = ((last_month_customers - previous_month_customers) / previous_month_customers) * 100
    else:
        customer_growth_percentage = 100 if last_month_customers > 0 else 0

    if customer_growth_percentage > 0:
        customer_growth_icon = 'fa-arrow-up'
        customer_growth_color = 'text-green-500 dark:text-green-500'
    elif customer_growth_percentage < 0:
        customer_growth_icon = 'fa-arrow-down'
        customer_growth_color = 'text-red-500 dark:text-red-500'
    else:
        customer_growth_icon = 'fa-minus'
        customer_growth_color = 'text-yellow-500 dark:text-yellow-500'

    current_year = timezone.now().year

    room_sales = Customer.objects.filter(
        check_in_date__year=current_year,
        is_active=False
    ).annotate(
        month=TruncMonth('check_in_date')
    ).values(
        'month', 'id', 'price_at_check_in', 'extra_bed', 'extra_bed_price_at_check_in'
    ).annotate(
        total=Sum('fee__amount'),
    ).order_by('month')

    for sale in room_sales:
        total_extra_items = 0
        total_extra_items_subtotal = 0
        purchase = Purchase.objects.filter(customer=sale['id']).first()
        if purchase:
            purchase_items = PurchaseItem.objects.filter(purchase=purchase)
            for item in purchase_items:
                total_extra_items += item.quantity
                total_extra_items_subtotal += item.price_at_purchase * item.quantity

        total_extra_items
        total_extra_items_subtotal
        total_extra_bed_subtotal = sale['extra_bed'] * sale['extra_bed_price_at_check_in']

        subtotal = sale['price_at_check_in'] + total_extra_items_subtotal + total_extra_bed_subtotal

        sale['total'] = subtotal

    walk_in_sales = PurchaseItem.objects.filter(
        purchase__created_at__year=current_year,
        purchase__is_walk_in=True,
        is_active=True
    ).annotate(
        total_price=F('price_at_purchase') * F('quantity'), 
        month=TruncMonth('purchase__created_at')  
    ).values(
        'month' 
    ).annotate(
        total=Sum('total_price')
    ).order_by('month')

    room_customer_counts = Customer.objects.filter(
        check_in_date__year=current_year,
        is_active=False
    ).annotate(
        month=TruncMonth('check_in_date')
    ).values('month').annotate(
        count=Count('id', distinct=True)
    ).order_by('month')

    walk_in_purchase_counts = Purchase.objects.filter(
        created_at__year=current_year,
        is_walk_in=True,
        is_active=True
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id', distinct=True)
    ).order_by('month')

    room_sales_data = [0] * 12
    walk_in_sales_data = [0] * 12

    customer_counts = [0] * 12 

    total_sales = 0
    total_customers = 0

    for sale in room_sales:
        month_index = sale['month'].month - 1
        room_sales_data[month_index] += float(sale['total']) or 0 
        total_sales += float(sale['total']) or 0

    for sale in walk_in_sales:
        month_index = sale['month'].month - 1
        walk_in_sales_data[month_index] = float(sale['total']) or 0 

        total_sales += float(sale['total']) or 0

    for count_data in room_customer_counts:
        month_index = count_data['month'].month - 1
        customer_counts[month_index] += count_data['count']
        total_customers += count_data['count']

    for count_data in walk_in_purchase_counts:
        month_index = count_data['month'].month - 1
        customer_counts[month_index] += count_data['count']
        total_customers += count_data['count']

    month_indicators = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    active_rooms = Customer.objects.filter(is_active=True)

    breadcrumbs = [
        ('Dashboard', None), 
    ]

    context = {
        'user': user,
        'breadcrumbs': breadcrumbs,
        'room_sales_data': room_sales_data,
        'walk_in_sales_data': walk_in_sales_data,
        'month_indicators': month_indicators,
        'total_sales': f'₱&nbsp;{total_sales:,.2f}',
        'active_rooms': active_rooms,
        'growth_percentage': f'{growth_percentage:.1f}%',
        'growth_icon': growth_icon,
        'growth_color': growth_color,
        'room_customer_counts': customer_counts,
        'total_customers': total_customers,
        'customer_growth_percentage': f'{customer_growth_percentage:.1f}%',
        'customer_growth_icon': customer_growth_icon,
        'customer_growth_color': customer_growth_color,
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
                next_url = request.GET.get('next', 'admin-dashboard')
                return redirect(next_url)
            else:
                error_message = 'Invalid username or password.'
    else:
        form = LoginForm() 

    return render(request, 'login.html', {'form': form, 'error_message': error_message})

@staff_required
@login_required
def user_management(request):
    users = User.objects.filter(is_active=True).order_by('-date_joined')

    breadcrumbs = [
        ('Dashboard', '/dashboard/'),
        ('User Management', None),
    ]

    context = {
        'users': users,
        'breadcrumbs': breadcrumbs
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

def handler403(request, exception):
    return render(request, 'errors/403.html', status=403)

def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    return render(request, 'errors/500.html', status=500)