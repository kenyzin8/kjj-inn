from django.db import models

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

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room.building.name} - {self.room.room_number} - {self.check_in_date} - {self.check_out_date}"

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
