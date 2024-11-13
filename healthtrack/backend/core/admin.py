# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, MedicalRecord, VitalSign, HealthcareProvider, ProviderAccess

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'phone_number')
    list_filter = ('is_staff', 'is_superuser', 'mfa_enabled')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'mfa_enabled')}),
    )

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'file_type', 'created_at')
    list_filter = ('file_type', 'created_at')
    search_fields = ('title', 'description', 'user__username')

@admin.register(VitalSign)
class VitalSignAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'measured_at', 'created_at')
    list_filter = ('type', 'measured_at')
    search_fields = ('user__username', 'notes')

@admin.register(HealthcareProvider)
class HealthcareProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'license_number', 'email')
    list_filter = ('specialty',)
    search_fields = ('name', 'license_number', 'email')

@admin.register(ProviderAccess)
class ProviderAccessAdmin(admin.ModelAdmin):
    list_display = ('provider', 'patient', 'granted_at', 'expires_at', 'is_active')
    list_filter = ('is_active', 'granted_at', 'expires_at')
    search_fields = ('provider__name', 'patient__username')