from django.contrib import admin
from apps.users.models import User
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone_number']
    list_filter = ['id', 'username', 'email', 'phone_number']
    search_fields = ['id', 'username', 'email', 'phone_number']