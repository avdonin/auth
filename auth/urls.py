"""auth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
#from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

from .views import signup, activate, HomeView
from . import views

urlpatterns = [
    path(r'', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('reset/<uidb64>/<token>/', views.password_reset, name='password_reset'),
    path('', HomeView.as_view(template_name='home.html'), name='home'),
]

handler404 = views.error_404_view
handler500 = views.error_500_view