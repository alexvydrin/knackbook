from django.urls import path

from likeapp.views import likes

app_name = "likeapp"

urlpatterns = [
    path('like/<int:pk>/', likes, name='like'),

]
