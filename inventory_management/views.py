from django.shortcuts import render, get_object_or_404
from .models import *
from room_management.models import Room, Customer
from django.contrib.auth.decorators import login_required
from core.decorators import staff_required
from django.http import JsonResponse
from django.db import transaction
import json
import uuid

def store(request):
    products = Product.objects.all()
    stocks = Stock.objects.all()
    active_customers = Customer.objects.filter(is_active=True)

    context = {
        'products': products,
        'stocks': stocks,
        'active_customers': active_customers
    }

    return render(request, 'store.html', context)

@login_required
def fetch_product(request):
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    product_barcode = request.GET.get('product_barcode')
    quantity = request.GET.get('quantity')

    if not product_barcode or not quantity:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

    if quantity == '0':
        return JsonResponse({'success': False, 'message': 'Invalid quantity'})

    try:
        barcode = Barcode.objects.get(barcode=product_barcode)
        stock = Stock.objects.get(product=barcode.product)
    except Barcode.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'})
    except Stock.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'})

    if not barcode:
        return JsonResponse({'success': False, 'message': 'Product not found'})

    if not stock:
        return JsonResponse({'success': False, 'message': 'Product not found'})

    if int(quantity) > int(stock.quantity):
        return JsonResponse({'success': False, 'message': 'Insufficient stock'})

    data = {
        'product_name': stock.product.name,
        'quantity': stock.quantity,
        'identifier': stock.identifier,
        'price': stock.get_price(),
        'stocks': stock.quantity,
        'price_unformatted': stock.price,
        'subtotal': stock.price * int(quantity),
    }

    return JsonResponse({'success': True, 'data': data})

@login_required
def submit_purchase(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    customer_id = request.POST.get('customer-id')

    if not customer_id:
        return JsonResponse({'success': False, 'message': 'Missing customer or room'})

    try:
        with transaction.atomic():
            if customer_id != 'walk-in':
                customer = Customer.objects.get(id=customer_id)
            else:
                customer = None

            purchase = Purchase.objects.create(customer=customer, is_walk_in=True if customer is None else False)

            cart_products_quantity = request.POST.getlist('cart-products-quantity[]')
            cart_products_identifier = request.POST.getlist('product-identifiers[]')

            if not cart_products_quantity or not cart_products_identifier:
                raise ValueError("Your cart is empty")

            for index, identifier in enumerate(cart_products_identifier):
                quantity = int(cart_products_quantity[index])
                stock = get_object_or_404(Stock, identifier=identifier)
                
                if stock.quantity < quantity:
                    raise ValueError("Not enough stock available")

                purchase_item = PurchaseItem.objects.create(purchase=purchase, stock=stock, quantity=quantity)

                stock.quantity -= quantity
                stock.save()

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': True, 'message': f'{purchase.get_purchase_number()} submitted successfully'})