from django.shortcuts import render
from .models import *

def store(request):
    products = Product.objects.all()
    stocks = Stock.objects.all()

    context = {
        'products': products,
        'stocks': stocks
    }

    return render(request, 'store.html', context)