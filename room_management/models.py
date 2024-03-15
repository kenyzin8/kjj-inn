from django.db import models
from django.utils import timezone

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
        return f"{self.building.name} - {self.room_number}"

    def get_room(self):
        return f"Room&nbsp;{self.room_number}"

    def get_good_for(self):
        plural = 's' if int(self.good_for) > 1 else ''
        a = f'{self.good_for}&nbsp;Person{plural}'
        return a

    def get_updated_at(self):
        self.updated_at = timezone.localtime(self.updated_at)
        return self.updated_at.strftime("%B %d, %Y - %I:%M %p")

    def get_updated_by(self):
        return f'{self.updated_by.first_name}&nbsp;{self.updated_by.last_name}'

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

class Customer(models.Model):
    alias = models.CharField(max_length=100, default="Anonymous")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    price_at_check_in = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room.building.name} - {self.room.room_number} - {self.check_in_date} - {self.check_out_date}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.price_at_check_in = self.room.room_type.fee.first().amount
        super(Customer, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
