from django.urls import path

from . import views

app_name = 'wardrobe'

urlpatterns = [
    path('', views.index, name='index')
]
