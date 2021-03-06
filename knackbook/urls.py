"""knackbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [

    path('admin/', admin.site.urls, name='admin'),

    path('', include('mainapp.urls', namespace='main')),

    path('auth/', include('authapp.urls', namespace='auth')),

    path('comments/', include('commentapp.urls', namespace='comments')),

    path('cabinet/', include('cabinetapp.urls', namespace='cabinet')),

    path('likes/', include('likeapp.urls', namespace='likes')),

    path('notification/', include('notificationapp.urls',
                                  namespace='notification')),

    path('captcha/', include('captcha.urls')),
    url(r'^favicon\.png$', RedirectView.as_view(
        url='/static/image/favicon.png',
        permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
