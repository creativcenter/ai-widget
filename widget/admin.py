from django.contrib import admin
from .models import User, Manager, Chat, Message

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'telegram_id')
    search_fields = ('username', 'telegram_id')

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active')
    list_filter = ('is_active',)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'manager', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'sender', 'timestamp')
    list_filter = ('timestamp',)
