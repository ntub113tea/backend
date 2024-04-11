from django.contrib import admin
from myapp.models import HerbStock
from myapp.models import Sale
from myapp.models import Purchase
from myapp.models import Customer

class HerbStockAdmin(admin.ModelAdmin):
    list_display=('herbs_id','herbs_name','current_stock')
    list_filter=('herbs_name',)

class PurchaseAdmin(admin.ModelAdmin):
    list_display=('purchases_id','herbs_id','purchases_value','purchases_time')
    #list_filter()
    ordering=('purchases_id',)

# Register your models here.
admin.site.register(HerbStock,HerbStockAdmin)
admin.site.register(Sale)
admin.site.register(Purchase,PurchaseAdmin)
admin.site.register(Customer)