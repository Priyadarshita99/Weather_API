"""
URL configuration for Project34 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path

from app.views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/',registration,name='registration'),
    path('user_login/',user_login,name='user_login'),
    path('home/',home,name='home'),
    path('user_logout/',user_logout,name='user_logout'),
    path('display_profile/',display_profile,name='display_profile'),
    path('change_password/',change_password,name='change_password'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('search/',search,name='search'),
    path('user_history/',user_history,name='user_history'),
    path('all_history/',all_history,name='all_history'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)