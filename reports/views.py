from django.shortcuts import render
from inventory_management.models import Purchase, PurchaseItem
from room_management.models import Customer
from django.contrib.auth.decorators import login_required
from core.decorators import staff_required

@login_required
@staff_required
def sales(request):
    walk_in_purchases = Purchase.objects.filter(customer=None)
    walk_in_purchase_items = PurchaseItem.objects.filter(purchase__in=walk_in_purchases)

    checked_out_rooms = Customer.objects.filter(is_active=False)

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