from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Client, Worker, Assignment

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active')  # Replace 'username' with 'email'
    list_filter = ('is_staff', 'is_active', 'is_client', 'is_worker')
    ordering = ('email',)  # Use 'email' instead of 'username'
    search_fields = ('email',)  # Use 'email' for searching

class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'state', 'LGA', 'phone_number')
    search_fields = ('company_name', 'state', 'LGA', 'phone_number')

class WorkerAdmin(admin.ModelAdmin):
    list_display = ('user', 'state', 'LGA', 'phone_number')
    search_fields = ('state', 'LGA', 'phone_number')

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('worker', 'client', 'assigned_at')
    search_fields = ('email', 'is_client', 'is_worker', 'assigned_at')
    list_filter = ('assigned_at',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(Assignment, AssignmentAdmin)
