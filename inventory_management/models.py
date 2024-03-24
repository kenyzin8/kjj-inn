from django.db import models
import uuid
from django.utils import timezone

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
    identifier = models.CharField(max_length=100, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def get_price(self):
        return f"₱&nbsp;{self.price:,.2f}"

    def save(self, *args, **kwargs):
        if not self.batch_no:
            last_batch_no = Stock.objects.all().order_by('batch_no').last()
            if not last_batch_no:
                self.batch_no = 1
            else:
                self.batch_no = last_batch_no.batch_no + 1

            self.identifier = uuid.uuid4().hex

        super(Stock, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

class Purchase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    is_walk_in = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def get_purchase_number(self):
        return f"{str(self.id).zfill(3)}"

    def get_total(self):
        total = 0
        for item in self.purchased_items.all():
            total += item.price_at_purchase * item.quantity

        return f"₱&nbsp;{total:,.2f}"

    def get_created_at(self):
        self.created_at = timezone.localtime(self.created_at)
        return self.created_at.strftime("%B %d, %Y %I:%M %p")

    def __str__(self):
        if self.is_walk_in:
            return f"Walk-in Purchase {self.id}"

        return f"Purchase {self.id} for {self.customer}"

    class Meta:
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='purchased_items', on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.stock.product.name} - {self.quantity}"

    def get_price_at_purchase(self):
        return f"₱&nbsp;{self.price_at_purchase:,.2f}"

    def get_total(self):
        return f"₱&nbsp;{self.price_at_purchase * self.quantity:,.2f}"

    def save(self, *args, **kwargs):
        if not self.price_at_purchase:
            self.price_at_purchase = self.stock.price
        
        super(PurchaseItem, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Purchase Item"
        verbose_name_plural = "Purchase Items"