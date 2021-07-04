import authapp.views as authapp
from django.urls import path

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    path('edit/', authapp.edit, name='edit'),
    path('delete-user/<int:pk>/', authapp.delete_user, name='delete_user'),
    path('edit-avatar/', authapp.edit_avatar, name='edit_avatar'),
]
