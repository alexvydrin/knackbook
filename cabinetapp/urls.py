from django.urls import path

from .views import main

app_name = "cabinetapp"

urlpatterns = [
    path('', main, name='cabinet'),
]
