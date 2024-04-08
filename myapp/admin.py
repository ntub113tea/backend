from django.contrib import admin
from myapp.models import HerbsStock
from myapp.models import Sale
from myapp.models import Purchases
from myapp.models import Customer


# Register your models here.
admin.site.register(HerbsStock)
admin.site.register(Sale)
admin.site.register(Purchases)
admin.site.register(Customer)