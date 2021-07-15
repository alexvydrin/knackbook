import authapp.views as authapp
from django.urls import path

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login_user, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    path('edit/', authapp.edit_user, name='edit'),
    path('delete-user/<int:pk>/', authapp.delete_user, name='delete_user'),
    path('ban-user/<int:pk>/<int:article>/', authapp.banned_user, name='ban_user'),
    path('edit-avatar/', authapp.edit_avatar, name='edit_avatar'),
    path('edit-password/', authapp.PasswordEditView.as_view(),
         name='edit_password'),
]
