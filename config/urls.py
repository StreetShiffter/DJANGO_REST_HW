from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("educations.urls", namespace="educations")),
    path("users/", include("users.urls", namespace="users")),
    # OpenAPI schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # UI документации
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # Дополнительно: Swagger UI по короткому пути /swagger/
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Безопасное определение корня статики
    static_root = getattr(settings, "STATIC_ROOT", None)
    if not static_root:
        staticfiles_dirs = getattr(settings, "STATICFILES_DIRS", [])
        if staticfiles_dirs:
            static_root = staticfiles_dirs[0]

    if static_root:
        urlpatterns += static(settings.STATIC_URL, document_root=static_root)
