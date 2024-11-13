# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, MedicalRecordViewSet, VitalSignViewSet,
    HealthcareProviderViewSet, ProviderAccessViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'medical-records', MedicalRecordViewSet, basename='medical-record')
router.register(r'vital-signs', VitalSignViewSet, basename='vital-sign')
router.register(r'providers', HealthcareProviderViewSet, basename='provider')
router.register(r'provider-access', ProviderAccessViewSet, basename='provider-access')

urlpatterns = [
    path('', include(router.urls)),
]

# healthtrack/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)