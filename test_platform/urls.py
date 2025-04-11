from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/', include('backend.urls')),
    path('admin/', include('custom_admin.urls')),
]
