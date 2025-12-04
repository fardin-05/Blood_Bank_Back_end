from django.contrib import admin
from django.urls import path,include
from user.views import ActiveUserAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('blood_app.urls')),

    #=======Djoser End-points===========
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    #=========User Activation Link==========
    path('activate/<uid>/<token>/', ActiveUserAPIView.as_view(), name='user_activate'),
    
    path('user/',include('user.urls')),

]
