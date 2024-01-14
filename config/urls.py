
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="BLOG API",

        description="mini service for posting your life",

        default_version="v1",
    ),
    public=True
)
0
urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('product.urls')),
    path('user/', include('user.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('category/', include('category.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

