from django.contrib import admin

# Register your models here.
from apps.websocket.models import ChatMessage

admin.site.register(ChatMessage)