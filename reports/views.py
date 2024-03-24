from django.shortcuts import render, redirect
from inventory_management.models import Purchase, PurchaseItem
from room_management.models import Customer, ExtraBedPrice
from django.contrib.auth.decorators import login_required
from core.decorators import staff_required

@login_required
@staff_required
def sales(request):
    start_date = request.GET.get('startDate')
    end_date = request.GET.get('endDate')

    walk_in_purchases = Purchase.objects.filter(customer=None)

    if start_date and end_date:
        walk_in_purchases = walk_in_purchases.filter(created_at__date__range=[start_date, end_date])

    walk_in_purchase_items = PurchaseItem.objects.filter(purchase__in=walk_in_purchases).order_by('-created_at')

    checked_out_rooms = Customer.objects.filter(is_active=False).order_by('-check_in_date')
    if start_date and end_date:
        checked_out_rooms = checked_out_rooms.filter(check_out_date__date__range=[start_date, end_date])

    for room in checked_out_rooms:
        total_extra_items = 0
        total_extra_items_subtotal = 0
        purchase = Purchase.objects.filter(customer=room).first()
        if purchase:
            purchase_items = PurchaseItem.objects.filter(purchase=purchase)
            for item in purchase_items:
                total_extra_items += item.quantity
                total_extra_items_subtotal += item.price_at_purchase * item.quantity

        room.total_extra_items = total_extra_items
        room.total_extra_items_subtotal = total_extra_items_subtotal

        total_extra_bed_subtotal = room.extra_bed * room.extra_bed_price_at_check_in

        subtotal = room.price_at_check_in + room.total_extra_items_subtotal + total_extra_bed_subtotal

        room.subtotal = f'₱&nbsp;{subtotal:,.2f}'

    breadcrumbs = [
        ('Dashboard', '/dashboard/'),
        ('Sales', None), 
    ]

    context = {
        'breadcrumbs': breadcrumbs,
        'walk_in_purchases': walk_in_purchases,
        'walk_in_purchase_items': walk_in_purchase_items,
        'checked_out_rooms': checked_out_rooms,
    }

    return render(request, 'sales.html', context)

@login_required
@staff_required
def view_sales(request, sale_slug):
    customer = Customer.objects.filter(slug=sale_slug).first()

    if not customer:
        return redirect('sales')

    purchases = Purchase.objects.filter(customer=customer, is_active=True).order_by('-created_at')
    purchase_items = PurchaseItem.objects.filter(purchase__in=purchases, is_active=True).order_by('created_at')

    total_purchase = 0
    for purchase_item in purchase_items:
        total_purchase += purchase_item.price_at_purchase * purchase_item.quantity
        purchase_item.total = f"₱&nbsp;{(purchase_item.price_at_purchase * purchase_item.quantity):,.2f}"

    total_price = customer.get_extra_bed_price_unformatted() + customer.fee.amount + total_purchase
    total_quantity = customer.extra_bed + 1 + sum([item.quantity for item in purchase_items])

    customer.total_price = f"₱&nbsp;{total_price:,.2f}"
    customer.total_quantity = total_quantity
    customer.grand_total =  f"₱&nbsp;{(total_price - customer.amount_paid):,.2f}"
    customer.grand_total_unformatted = total_price - customer.amount_paid

    extra_bed = ExtraBedPrice.objects.first()

    breadcrumbs = [
        ('Dashboard', '/dashboard/'),
        ('Sales', '/reports/sales/'),
        (f'{customer.room} Summary', None), 
    ]

    context = {
        'customer': customer,
        'breadcrumbs': breadcrumbs,
        'purchases': purchases,
        'purchase_items': purchase_items,
        'extra_bed': extra_bed,
    }

    return render(request, 'view_sales.html', context)