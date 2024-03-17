from django.db import models

# Create your models here.
from room_management.models import Customer

class ProductType(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Type"
        verbose_name_plural = "Product Types"

class Product(models.Model):
    name = models.CharField(max_length=100)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

class Barcode(models.Model):
    barcode = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.barcode

    class Meta:
        verbose_name = "Barcode"
        verbose_name_plural = "Barcodes"

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    barcodes = models.ManyToManyField(Barcode, blank=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    batch_no = models.IntegerField(blank=True)
    expiry_date = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def save(self, *args, **kwargs):
        if not self.batch_no:
            last_batch_no = Stock.objects.all().order_by('batch_no').last()
            if not last_batch_no:
                self.batch_no = 1
            else:
                self.batch_no = last_batch_no.batch_no + 1
        super(Stock, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"


class Purchase(models.Model):
    products_bought = models.ManyToManyField(Stock, blank=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.stock.product.name} - {self.quantity}"

    class Meta:
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"

