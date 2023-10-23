from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chargers/',include('api.chargers.urls')),
    path('api/users/',include('api.users.urls')),
    path('api/auth/', include('api.auth.urls'))
]
