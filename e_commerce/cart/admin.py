from django.contrib import admin
from .models import Cart, Order, OrderProduct

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'date_added')
    list_filter = ('user', 'product')
    search_fields = ('user__username', 'product__title')

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_code', 'status', 'total', 'date_ordered')
    list_filter = ('user', 'status', 'date_ordered')
    search_fields = ('user__username', 'order_code', 'country', 'city', 'address', 'phone', 'zip_code', 'adminnote')
    inlines = [OrderProductInline]

admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
