from django.db import models
from django.utils import timezone

import uuid

class Building(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_building(self):
        nbsp = self.name.replace(' ', '&nbsp;')
        return nbsp

    def get_rooms(self):
        return self.room_set.filter(is_active=True)

    def get_active_room_count(self):
        active_rooms = Customer.objects.filter(is_active=True, room__building=self).count()
        plural = 's' if active_rooms != 1 else ''
        return f'{active_rooms} Room{plural} Occupied'

    def get_active_room_count_number(self):
        return Customer.objects.filter(is_active=True, room__building=self).count()

    class Meta:
        verbose_name = "Building"
        verbose_name_plural = "Buildings"

class Fee(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    hours = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hours} hours - {self.amount}"

    def get_updated_at(self):
        self.updated_at = timezone.localtime(self.updated_at)
        return self.updated_at.strftime("%B %d, %Y - %I:%M %p")

    def get_hours(self):
        plural = 's' if int(self.hours) > 1 else ''
        a = f"{self.hours}&nbsp;Hour{plural}"
        return a

    def get_amount(self):
        self.amount = f"{self.amount:,.2f}"
        return f"₱&nbsp;{self.amount}"

    def get_room_type(self):
        room_types = self.roomtype_set.all() 
        return ', '.join([rt.name for rt in room_types]) if room_types else 'N/A'

    class Meta:
        verbose_name = "Fee"
        verbose_name_plural = "Fees" 

class RoomType(models.Model):
    name = models.CharField(max_length=100)
    fee = models.ManyToManyField(Fee, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_updated_at(self):
        self.updated_at = timezone.localtime(self.updated_at)
        return self.updated_at.strftime("%B %d, %Y - %I:%M %p")

    def get_fees(self):
        fees = self.fee.all()
        return ', '.join([f"{f.hours} hours - ₱{f.amount:,.2f}" for f in fees]) if fees else 'N/A'

    class Meta:
        verbose_name = "Room Type"
        verbose_name_plural = "Room Types"

class Room(models.Model):
    room_number = models.IntegerField()
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    good_for = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.building.name} - Room {self.room_number}"

    def get_room(self):
        return f"Room&nbsp;{self.room_number}"

    def get_room_for_dropdown(self):
        return f"{self.building.name} - Room {self.room_number}"

    def get_good_for(self):
        plural = 's' if int(self.good_for) > 1 else ''
        a = f'{self.good_for}&nbsp;Person{plural}'
        return a

    def get_updated_at(self):
        self.updated_at = timezone.localtime(self.updated_at)
        return self.updated_at.strftime("%B %d, %Y - %I:%M %p")

    def get_updated_by(self):
        return f'{self.updated_by.first_name}&nbsp;{self.updated_by.last_name}'

    def is_room_occupied(self):
        return Customer.objects.filter(room=self, is_active=True).exists()

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

class Customer(models.Model):
    alias = models.CharField(max_length=100, default="Anonymous")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, blank=True, null=True)
    check_in_date = models.DateTimeField(auto_now_add=True)
    check_out_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_at_check_in = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    plate_number = models.CharField(max_length=10, blank=True, null=True)
    extra_bed = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    slug = models.SlugField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.room.building.name} - {self.room.room_number} - {self.check_in_date} - {self.check_out_date}"

    def get_extra_bed_price(self):
        extra_bed_price = ExtraBedPrice.objects.first()
        total = self.extra_bed * extra_bed_price.price
        return f"₱&nbsp;{total:,.2f}"

    def get_room_price(self):
        return f"₱&nbsp;{self.price_at_check_in:,.2f}"

    def get_amount_paid(self):
        return f"₱&nbsp;{self.amount_paid:,.2f}"

    def get_extra_bed_price_unformatted(self):
        extra_bed_price = ExtraBedPrice.objects.first()
        total = self.extra_bed * extra_bed_price.price
        return total

    def get_room_price_unformatted(self):
        return self.price_at_check_in

    def unformatted_get_remaining_time(self):
        self.check_out_date = timezone.localtime(self.check_out_date)
        remaining_time = max(self.check_out_date - timezone.now(), timezone.timedelta(seconds=0))
        total_seconds = remaining_time.total_seconds()
        hours, remainder = divmod(remaining_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_time = f"{int(hours)}hrs {int(minutes)}mins {int(seconds)}secs"
        return formatted_time if total_seconds > 0 else "end"

    def get_remaining_time(self):
        self.check_out_date = timezone.localtime(self.check_out_date)
        remaining_time = max(self.check_out_date - timezone.now(), timezone.timedelta(seconds=0))
        hours, remainder = divmod(remaining_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        parts = []
        if hours:
            parts.append(f"{int(hours)}hr{'s' if hours != 1 else ''}")
        if hours or minutes:
            parts.append(f"{int(minutes)}min{'s' if minutes != 1 else ''}")
        parts.append(f"{int(seconds)}sec{'s' if seconds != 1 else ''}")
        return ' '.join(parts)

    def get_formatted_check_out_date(self):
        self.check_out_date = timezone.localtime(self.check_out_date)
        return self.check_out_date.strftime("%B %d, %Y - %I:%M %p")

    def get_formatted_check_in_date(self):
        self.check_in_date = timezone.localtime(self.check_in_date)
        return self.check_in_date.strftime("%B %d, %Y - %I:%M %p")

    def save(self, *args, **kwargs):
        if not self.id:
            self.price_at_check_in = self.room.room_type.fee.first().amount
        
        self.slug = uuid.uuid4().hex
        
        super(Customer, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

class ExtraBedPrice(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"₱{self.price:,.2f}"

    def get_updated_at(self):
        self.updated_at = timezone.localtime(self.updated_at)
        return self.updated_at.strftime("%B %d, %Y - %I:%M %p")

    class Meta:
        verbose_name = "Extra Bed Price"
        verbose_name_plural = "Extra Bed Prices"