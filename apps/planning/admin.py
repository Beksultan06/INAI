from django.contrib import admin

from apps.planning.models import Route, Vehicle

# Register your models here.
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'license_plate', 'capacity', 'available', 'created_at']
    list_filter = ['available']
    search_fields = ['name', 'license_plate']

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['order', 'vehicle', 'courier', 'start_location', 'end_location', 'status', 'distance', 'estimated_time', 'cost']
    list_filter = ['status', 'courier', 'vehicle']
    search_fields = ['order__id', 'courier__username', 'vehicle__license_plate']
    actions = ['mark_completed']

    def mark_completed(self, request, queryset):
        for route in queryset:
            route.complete_route()
        self.message_user(request, "Выбранные маршруты отмечены как завершённые.")
    mark_completed.short_description = "Отметить как завершённые"
