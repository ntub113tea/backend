from django.contrib import admin
from .models import Customer
from myapp.models import HerbStock
from myapp.models import Sale
from myapp.models import Purchase
from myapp.models import Customer

class HerbStockAdmin(admin.ModelAdmin):
    list_display=('herbs_id','herbs_name','current_stock')
    list_filter=('herbs_name',)
    ordering=('herbs_id',)

class PurchaseAdmin(admin.ModelAdmin):
    list_display=('purchases_id','herbs_id','herbs_name','purchases_value','purchases_time')
    #list_filter()
    ordering=('purchases_id',)

class SaleAdmin(admin.ModelAdmin):
    list_display=('sale_id','customer_id','herbs_id','product_name','order_time')
    ordering=('sale_id',)

class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display=('customer_id','customer_name','sex','age','line_id')
    ordering=('customer_id',)


# Register your models here.
admin.site.register(HerbStock,HerbStockAdmin)
admin.site.register(Sale,SaleAdmin)
admin.site.register(Purchase,PurchaseAdmin)
admin.site.register(Customer,CustomerAdmin)