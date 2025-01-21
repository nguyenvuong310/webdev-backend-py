
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from dotenv import load_dotenv
import os
load_dotenv()

schema_view = get_schema_view(
    openapi.Info(
        title="Gscores",
        default_version='v1',
        description="Gscores API description",
        contact=openapi.Contact(email="trugnvuong2169@gmail.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url = os.getenv('API_URL')
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('scores.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('documentation/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
