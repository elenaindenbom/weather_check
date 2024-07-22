from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('weather.urls', namespace='weather')),
    path('admin/', admin.site.urls),
]
