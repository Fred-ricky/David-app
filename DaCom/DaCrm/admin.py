from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Client, Worker, Assignment

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'user_type')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'state', 'lga', 'phone_number')
    search_fields = ('user__username', 'company_name', 'state', 'lga', 'phone_number')

class WorkerAdmin(admin.ModelAdmin):
    list_display = ('user', 'state', 'lga', 'phone_number')
    search_fields = ('user__username', 'first_name', 'last_name', 'state', 'lga', 'phone_number')

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('worker', 'client', 'assigned_at')
    search_fields = ('worker__user__username', 'client__user__username', 'assigned_at')
    list_filter = ('assigned_at',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(Assignment, AssignmentAdmin)
