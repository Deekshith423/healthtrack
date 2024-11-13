# api/serializers.py
from rest_framework import serializers
from core.models import User, MedicalRecord, VitalSign, HealthcareProvider, ProviderAccess

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'phone_number', 'mfa_enabled', 'created_at')
        read_only_fields = ('id', 'created_at')

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

class VitalSignSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = VitalSign
        fields = ('id', 'type', 'type_display', 'value', 'measured_at', 
                 'device_id', 'notes', 'created_at')
        read_only_fields = ('id', 'created_at')

class HealthcareProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthcareProvider
        fields = ('id', 'name', 'specialty', 'license_number', 
                 'email', 'phone', 'created_at')
        read_only_fields = ('id', 'created_at')

class ProviderAccessSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)

    class Meta:
        model = ProviderAccess
        fields = ('id', 'provider', 'provider_name', 'patient', 'patient_name',
                 'granted_at', 'expires_at', 'is_active')
        read_only_fields = ('id', 'granted_at')