from django.db import models
import uuid

MAX_BOOKINGS = 2    # Maximum booking allowed per member


class Member(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    booking_count = models.IntegerField(default=0)
    date_joined = models.DateTimeField()

    def __str__(self):
        return f"{self.name} {self.surname} ({self.booking_count} bookings)"


class Inventory(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    remaining_count = models.IntegerField()
    expiration_date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.remaining_count} available"


class Bookings(models.Model):
    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bookings {self.reference} - {self.member} -> {self.inventory}"