from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from apps.base.models import Order, Product, OrderProduct, ExtendedOrder

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created_at']
    list_filter = ['status', ('created_at', DateFieldListFilter)]
    search_fields = ['user__username', 'status']
    list_editable = ['status']

    actions = ['mark_as_processed']

    def mark_as_processed(self, request, queryset):
        queryset.update(status='processed')
        self.message_user(request, "Выбранные заказы отмечены как обработанные.")
    mark_as_processed.short_description = "Отметить как обработанные"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Основная информация", {
            'fields': ('title', 'descriptions', 'price')
        }),
        ("Дополнительно", {
            'fields': ('photo', 'created_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ['created_at']

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_filter = ['id', 'order', 'product', 'quantity']
    search_fields = ['id', 'order', 'product', 'quantity']

    list_display = ['id', 'order', 'product', 'quantity', 'link_to_order', 'link_to_product']

    def link_to_order(self, obj):
        from django.utils.html import format_html
        return format_html('<a href="/admin/apps.base/order/{}/change/">Посмотреть заказ</a>', obj.order.id)
    link_to_order.short_description = "Заказ"

    def link_to_product(self, obj):
        from django.utils.html import format_html
        return format_html('<a href="/admin/apps.base/product/{}/change/">Посмотреть продукт</a>', obj.product.id)
    link_to_product.short_description = "Продукт"

@admin.register(ExtendedOrder)
class ExtendedOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'courier']
    list_filter = ['id', 'client', 'courier']
    search_fields = ['id', 'client', 'courier']