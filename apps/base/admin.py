from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from apps.base.models import Order

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