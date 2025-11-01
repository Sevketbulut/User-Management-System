from django.contrib import admin
from .models import User, UserLog

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'role', 'department', 'status', 'created_at')
    list_filter = ('role', 'status', 'department')
    search_fields = ('name', 'email', 'department')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')#tarihlerin elle değiştirilmesini engelliyor.
    list_per_page = 25

@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'performed_by', 'timestamp')
    list_filter = ('action', 'performed_by')
    search_fields = ('user__name', 'user__email', 'performed_by')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
