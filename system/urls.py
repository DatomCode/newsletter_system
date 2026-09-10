from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Newsletter API
    path('api/', include('subscribe_service.urls')),

    # OpenAPI schema (raw JSON/YAML)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI  →  /api/docs/
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # ReDoc UI  →  /api/redoc/
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
