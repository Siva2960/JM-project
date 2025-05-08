from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import SupportEntry, pas_Entry, RideRequest

admin.site.register(SupportEntry)
admin.site.register(pas_Entry)
admin.site.register(RideRequest)
