from django.contrib import admin
from .models import Product, Order, OrderItem
from django.utils.html import format_html

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'get_items', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at',)
    list_editable = ('status',)
    search_fields = ('name', 'phone')
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]

    def colored_status(self, obj):
        colors = {
            'Pending': 'orange',
            'Processing': 'blue',
            'Delivered': 'green',
            'Cancelled': 'red',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.status,
        )
    colored_status.short_description = 'STATUS'
    colored_status.admin_order_field = 'status'
        

    def get_items(self, obj):
        order_items = obj.items.all()
        return ",".join([str(item) for item in order_items])
    
    get_items.short_description = 'Product Ordered'




# Register your models here.S

