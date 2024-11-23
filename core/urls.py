from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.base.views import main, active_orders
from apps.users.views import register, login, kura_user

schema_view = get_schema_view(
    openapi.Info(
        title="INAI",
        default_version='v1',
        description="INAI description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="nurlanuuulubeksultan@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns_page = [
    path('', main, name='orders-page'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path("active_orders", active_orders, name='active_orders'),
    path("kura_user", kura_user, name='kura_user')
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/users/", include("apps.users.urls")),
    path("api/v1/base/", include("apps.base.urls")),
    path("api/v1/planning/", include("apps.planning.urls")),

    # Swagger и Redoc
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("", include(urlpatterns_page))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
