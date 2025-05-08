from django.db import models

class signin(models.Model):
    USER_TYPE_CHOICES = [
        ('driver', 'Driver'),
        ('passenger', 'Passenger'),
    ]

    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name} ({self.user_type})"

    class Meta:
        db_table = 'jmate_signin'  # Use your actual DB table name
        managed = False  # VERY IMPORTANT!













class SupportEntry(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    user_type = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=20)

    # From Location
    support_info = models.TextField()  # Original input (area name / URL / coordinates)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    area_name = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)

    # To Location
    to_location = models.TextField()  # Original input
    to_latitude = models.FloatField(null=True, blank=True)
    to_longitude = models.FloatField(null=True, blank=True)
    to_area = models.CharField(max_length=100, null=True, blank=True)
    to_pincode = models.CharField(max_length=10, null=True, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)
    request_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.number})"
    class Meta:
        db_table = 'jmate_SupportEntry'  # Use your actual DB table name
        managed = False  # VERY IMPORTANT!



#passanger dat model

from django.db import models

class pas_Entry(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    user_type = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=20)

    # From Location
    support_info = models.TextField()  # Original input (area name / URL / coordinates)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    area_name = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)

    # To Location
    to_location = models.TextField()  # Original input
    to_latitude = models.FloatField(null=True, blank=True)
    to_longitude = models.FloatField(null=True, blank=True)
    to_area = models.CharField(max_length=100, null=True, blank=True)
    to_pincode = models.CharField(max_length=10, null=True, blank=True)
    passengers = models.PositiveIntegerField(default=1)

    # Ride status & Assignment
    status = models.CharField(
        max_length=20,
        default='pending',  # Options: waiting, picked, completed
        choices=[
            ('pending', 'Pending'),
            ('picked', 'Picked'),
            ('completed', 'Completed')
        ]
    )

    assigned_driver = models.CharField(
        max_length=15,
        null=True,
        blank=True  # This could be the driver's phone number or user ID
    )

    # Time when the passenger information is submitted
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.number})"

    class Meta:
        db_table = 'jmate_pas_Entry'  # or any custom name
        managed = True  # if true is here ,Allow Django to change the table



from django.db import models
from .models import SupportEntry, pas_Entry  # adjust import path if needed
class RideRequest(models.Model):
    passenger = models.ForeignKey(pas_Entry, on_delete=models.CASCADE)
    driver = models.ForeignKey(SupportEntry, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request from {self.passenger.name} to {self.driver.name} [{self.status}]"
