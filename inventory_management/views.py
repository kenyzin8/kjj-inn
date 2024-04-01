from django.shortcuts import render, get_object_or_404
from .models import *
from room_management.models import Room, Customer
from django.contrib.auth.decorators import login_required
from core.decorators import staff_required, rate_limit
from django.http import JsonResponse
from django.db import transaction
import json
import uuid
from django.db.models.functions import Lower, Trim

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
@rate_limit(50, 'min')
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

@login_required
@staff_required
def manage_product_types(request):
    product_types = ProductType.objects.filter(is_active=True).order_by('name')

    context = {
        'product_types': product_types
    }

    return render(request, 'manage/product_types.html', context)

@login_required
@staff_required
def add_product_type(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    name = request.POST.get('product-type')

    if not name:
        return JsonResponse({'success': False, 'message': 'Invalid name'})

    trimmed_name = name.strip().lower()

    exist = ProductType.objects.annotate(
        trimmed_name=Lower(Trim('name'))
    ).filter(
        trimmed_name=trimmed_name
    ).exists()

    if exist:
        return JsonResponse({'success': False, 'message': 'Product type already exists', 'product_type_exists': True})

    try:
        product_type = ProductType.objects.create(name=name)
        data = {
            'id': product_type.id,
            'name': product_type.name
        }
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': True, 'message': f'Product type added successfully', 'data': data})

@login_required
@staff_required
def update_product_type(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    product_type_id = request.POST.get('product-type-id')
    name = request.POST.get('product-type')

    if not product_type_id or not name:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

    trimmed_name = name.strip().lower()

    exist = ProductType.objects.annotate(
        trimmed_name=Lower(Trim('name'))
    ).filter(
        trimmed_name=trimmed_name
    ).exclude(
        id=product_type_id
    ).exists()

    if exist:
        return JsonResponse({'success': False, 'message': 'Product type already exists', 'product_type_exists': True})

    product_type = get_object_or_404(ProductType, id=product_type_id)

    try:
        product_type.name = name
        product_type.save()
        data = {
            'id': product_type.id,
            'name': product_type.name
        }
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': True, 'message': f'Product type updated successfully', 'data': data})

@login_required
@staff_required
def delete_product_type(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    body = json.loads(request.body)
    product_type_id = body.get('id')

    if not product_type_id:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

    product_type = get_object_or_404(ProductType, id=product_type_id)

    try:
        product_type.is_active = False
        product_type.save()
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': True, 'message': f'Product type deleted successfully'})

@login_required
@staff_required
def manage_products(request):
    products = Product.objects.filter(is_active=True).order_by('name')
    product_types = ProductType.objects.filter(is_active=True).order_by('name')

    context = {
        'products': products,
        'product_types': product_types
    }

    return render(request, 'manage/products.html', context)

@login_required
@staff_required
def add_product(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    name = request.POST.get('product-name')
    product_type_id = request.POST.get('product-type')

    if not name or not product_type_id:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

    trimmed_name = name.strip().lower()

    exist = Product.objects.annotate(
        trimmed_name=Lower(Trim('name'))
    ).filter(
        trimmed_name=trimmed_name, 
        product_type_id=product_type_id
    ).exists()

    if exist:
        return JsonResponse({'success': False, 'message': 'Product already exists', 'product_exists': True})

    product_type = get_object_or_404(ProductType, id=product_type_id)

    try:
        product = Product.objects.create(name=name, product_type=product_type)
        data = {
            'id': product.id,
            'name': product.name,
            'product_type': product.product_type.name
        }
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': True, 'message': f'Product added successfully', 'data': data})

@login_required
@staff_required
def update_product(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    product_id = request.POST.get('product-id')
    name = request.POST.get('product-name')
    product_type_id = request.POST.get('product-type')

    if not product_id or not name or not product_type_id:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

    trimmed_name = name.strip().lower()

    exist = Product.objects.annotate(
        trimmed_name=Lower(Trim('name'))
    ).filter(
        trimmed_name=trimmed_name, 
        product_type_id=product_type_id
    ).exclude(
        id=product_id
    ).exists()

    if exist:
        return JsonResponse({'success': False, 'message': 'Product already exists', 'product_exists': True})

    product = get_object_or_404(Product, id=product_id)
    product_type = get_object_or_404(ProductType, id=product_type_id)

    try:
        product.name = name
        product.product_type = product_type
        product.save()
        data = {
            'id': product.id,
            'name': product.name,
            'product_type': product.product_type.name,
            'product_type_id': product.product_type.id
        }
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': True, 'message': f'Product updated successfully', 'data': data})

@login_required
@staff_required
def delete_product(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    body = json.loads(request.body)
    product_id = body.get('id')

    if not product_id:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

    product = get_object_or_404(Product, id=product_id)

    try:
        product.is_active = False
        product.save()
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': True, 'message': f'Product deleted successfully'})

@login_required
@staff_required
def manage_barcodes(request):
    barcodes = Barcode.objects.filter(is_active=True).order_by('barcode')
    products = Product.objects.filter(is_active=True).order_by('name')

    context = {
        'barcodes': barcodes,
        'products': products
    }

    return render(request, 'manage/barcodes.html', context)

@login_required
@staff_required
def add_barcode(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    barcode = request.POST.get('barcode')
    product_id = request.POST.get('product')

    if not barcode or not product_id:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

    trimmed_barcode = barcode.strip().lower()

    exist = Barcode.objects.annotate(
        trimmed_barcode=Lower(Trim('barcode'))
    ).filter(
        trimmed_barcode=trimmed_barcode
    ).exists()

    if exist:
        return JsonResponse({'success': False, 'message': 'Barcode already exists', 'barcode_exists': True})

    product = get_object_or_404(Product, id=product_id)

    try:
        barcode = Barcode.objects.create(barcode=barcode, product=product)
        data = {
            'id': barcode.id,
            'barcode': barcode.barcode,
            'product': barcode.product.name,
            'product_id': barcode.product.id
        }
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': True, 'message': f'Barcode added successfully', 'data': data})

@login_required
@staff_required
def update_barcode(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    barcode_id = request.POST.get('barcode-id')
    new_barcode = request.POST.get('barcode')

    if not barcode_id or not new_barcode:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

    trimmed_barcode = new_barcode.strip().lower()

    exist = Barcode.objects.annotate(
        trimmed_barcode=Lower(Trim('barcode'))
    ).filter(
        trimmed_barcode=trimmed_barcode
    ).exclude(
        id=barcode_id
    ).exists()

    if exist:
        return JsonResponse({'success': False, 'message': 'Barcode already exists', 'barcode_exists': True})

    barcode = get_object_or_404(Barcode, id=barcode_id)

    try:
        barcode.barcode = new_barcode
        barcode.save()
        data = {
            'id': barcode.id,
            'barcode': barcode.barcode,
            'product': barcode.product.name,
            'product_id': barcode.product.id
        }
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': True, 'message': f'Barcode updated successfully', 'data': data})

@login_required
@staff_required
def delete_barcode(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    body = json.loads(request.body)
    barcode_id = body.get('id')

    if not barcode_id:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

    barcode = get_object_or_404(Barcode, id=barcode_id)

    try:
        barcode.is_active = False
        barcode.save()
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': True, 'message': f'Barcode deleted successfully'})

@login_required
@staff_required
def manage_stocks(request):
    stocks = Stock.objects.filter(is_active=True).order_by('product__name')
    products = Product.objects.filter(is_active=True).order_by('name')

    context = {
        'stocks': stocks,
        'products': products
    }

    return render(request, 'manage/stocks.html', context)

@login_required
@staff_required
def add_stock(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    product_id = request.POST.get('product')
    quantity = request.POST.get('quantity')
    price = request.POST.get('price')

    if not product_id or not quantity or not price:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

    product = get_object_or_404(Product, id=product_id)

    exist = Stock.objects.filter(product=product, is_active=True).exists()

    if exist:
        return JsonResponse({'success': False, 'message': 'Stock already exists', 'stock_exists': True})
    
    stock = Stock.objects.create(product=product, quantity=int(quantity), price=float(price))
    data = {
        'id': stock.id,
        'product': stock.product.name,
        'product_id': stock.product.id,
        'quantity': stock.quantity,
        'price': str(stock.get_price()),
        'price_unformatted': stock.price
    }

    return JsonResponse({'success': True, 'message': f'Stock added successfully', 'data': data})

@login_required
@staff_required
def update_stock(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    stock_id = request.POST.get('stock-id')
    quantity = request.POST.get('quantity')
    price = request.POST.get('price')

    if not stock_id or not quantity or not price:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

    stock = get_object_or_404(Stock, id=stock_id)

    try:
        stock.quantity = int(quantity)
        stock.price = float(price)
        stock.save()
        data = {
            'id': stock.id,
            'product': stock.product.name,
            'product_id': stock.product.id,
            'quantity': stock.quantity,
            'price': str(stock.get_price()),
            'price_unformatted': stock.price
        }
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': True, 'message': f'Stock updated successfully', 'data': data})

@login_required
@staff_required
def delete_stock(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    body = json.loads(request.body)
    stock_id = body.get('id')

    if not stock_id:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

    stock = get_object_or_404(Stock, id=stock_id)

    try:
        stock.is_active = False
        stock.save()
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': True, 'message': f'Stock deleted successfully'})