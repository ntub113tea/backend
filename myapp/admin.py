from django.contrib import admin
from .models import Customer
from myapp.models import HerbStock
from myapp.models import Sale
from myapp.models import Purchase
from myapp.models import Customer
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
User = get_user_model

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

class CustomerAdmin(UserAdmin):
    model = Customer
    list_display=('customer_id','customer_name','sex','age','line_id')
    fieldsets= (
        (None, {'fields': ('customer_id', 'password', 'customer_name', 'sex', 'age', 'line_id' , 'is_active', 'is_staff', 'is_superuser',)}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('customer_id', 'password1', 'password2', 'customer_name', 'sex', 'age', 'line_id', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    ordering=('customer_id',)


# Register your models here.
admin.site.register(HerbStock,HerbStockAdmin)
admin.site.register(Sale,SaleAdmin)
admin.site.register(Purchase,PurchaseAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.site_header = '侍茶師後台'
admin.site.site_title = '侍茶師後台'