"""
urls for notificationapp
"""

from django.urls import path
from notificationapp.views import notifications, notification_edit, \
    notification_delete

app_name = "notificationapp"

urlpatterns = [
    path('', notifications, name='notification'),
    path('notification_edit/<int:pk>/', notification_edit,
         name='notification_edit'),
    path('notification_delete/<int:pk>/', notification_delete,
         name='notification_delete'),
]
