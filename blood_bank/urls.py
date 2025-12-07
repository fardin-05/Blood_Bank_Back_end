from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from user.views import ActiveUserAPIView

schema_view = get_schema_view(
   openapi.Info(
      title="Blood Bank API",
      default_version='v1',
      description="API documentation for Blood Bank project",
      contact=openapi.Contact(email="fardinazim7@gmail.com"),
      license=openapi.License(name="MIT"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('blood_app.urls')),

    #=======Djoser End-points===========
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    #=========User Activation Link==========
    path('activate/<uid>/<token>/', ActiveUserAPIView.as_view(), name='user_activate'),
    path('user/',include('user.urls')),

    #====Swagger UI=======
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
