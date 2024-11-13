# api/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from core.models import User, MedicalRecord, VitalSign, HealthcareProvider, ProviderAccess
from .serializers import (
    UserSerializer, MedicalRecordSerializer, VitalSignSerializer,
    HealthcareProviderSerializer, ProviderAccessSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=True, methods=['get'])
    def vital_signs(self, request, pk=None):
        user = self.get_object()
        vital_signs = VitalSign.objects.filter(user=user)
        serializer = VitalSignSerializer(vital_signs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def medical_records(self, request, pk=None):
        user = self.get_object()
        records = MedicalRecord.objects.filter(user=user)
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)

class MedicalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MedicalRecord.objects.all()
        # Include records where user is the owner or where a provider has access
        provider_access = ProviderAccess.objects.filter(
            provider__in=user.healthcareprovider_set.all(),
            is_active=True
        ).values_list('patient', flat=True)
        return MedicalRecord.objects.filter(
            models.Q(user=user) | models.Q(user__in=provider_access)
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class VitalSignViewSet(viewsets.ModelViewSet):
    serializer_class = VitalSignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return VitalSign.objects.all()
        provider_access = ProviderAccess.objects.filter(
            provider__in=user.healthcareprovider_set.all(),
            is_active=True
        ).values_list('patient', flat=True)
        return VitalSign.objects.filter(
            models.Q(user=user) | models.Q(user__in=provider_access)
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HealthcareProviderViewSet(viewsets.ModelViewSet):
    serializer_class = HealthcareProviderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = HealthcareProvider.objects.all()

    @action(detail=True, methods=['post'])
    def grant_access(self, request, pk=None):
        provider = self.get_object()
        patient_id = request.data.get('patient_id')
        expires_at = request.data.get('expires_at')

        if not patient_id:
            return Response(
                {'error': 'patient_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        patient = get_object_or_404(User, id=patient_id)
        access, created = ProviderAccess.objects.get_or_create(
            provider=provider,
            patient=patient,
            defaults={'expires_at': expires_at}
        )

        serializer = ProviderAccessSerializer(access)
        return Response(serializer.data)

class ProviderAccessViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderAccessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ProviderAccess.objects.all()
        return ProviderAccess.objects.filter(
            models.Q(patient=user) | 
            models.Q(provider__in=user.healthcareprovider_set.all())
        )