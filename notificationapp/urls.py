from django.urls import path

from notificationapp.views import notifications

app_name = "notificationapp"

urlpatterns = [
    path('', notifications, name='notification'),
]
