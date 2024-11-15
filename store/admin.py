from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Design, Collection, Order,Review

admin.site.register(Design)
admin.site.register(Collection)
admin.site.register(Order)
admin.site.register(Review)