"""TPW_goclubbing URL Configuration

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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from app.views import index, search, searchName,dashboard, dashboard_profile, dashboard_home, register

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='auth.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', register),
    path('admin/', admin.site.urls),
    path('', index),
    path('search/', search),
    path('search/<str:id>', searchName),
    path('dashboard', dashboard, name='dashboard'),
    path('dashboard/profile', dashboard_profile, name='dashboard_profile'),
    path('dashboard/home', dashboard_home, name="dashboard_home")
]
