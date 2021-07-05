from django.urls import path

from .views import main, new_article

app_name = "cabinetapp"

urlpatterns = [
    path('', main, name='cabinet'),
    path('new-article/', new_article, name='new_article'),
]
