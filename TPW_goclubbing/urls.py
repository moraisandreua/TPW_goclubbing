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
from app.views import index, search, searchName, dashboard_profile, dashboard_home, dashboard_newevent, dashboard_event, dashboard_newad, dashboard_ad, register, dashboard_my_events, dashboard_my_ads, dashboard_my_comments, dashboard_delete
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='auth.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', register),
    path('admin/', admin.site.urls),
    path('', index),
    path('search/', search, name='search'),
    path('search/<int:id>/', searchName),
    path('dashboard/', dashboard_home, name='dashboard_home'),
    path('dashboard/profile', dashboard_profile, name='dashboard_profile'),
    path('dashboard/newevent', dashboard_newevent, name='dashboard_newevent'),
    path('dashboard/event/<int:num>', dashboard_event, name='dashboard_event'),
    path('dashboard/newad', dashboard_newad, name='dashboard_newad'),
    path('dashboard/ad/<int:num>', dashboard_ad, name='dashboard_ad'),
    path('dashboard/events', dashboard_my_events, name='dashboard_my_events'),
    path('dashboard/ads', dashboard_my_ads, name='dashboard_my_ads'),
    path('dashboard/comments', dashboard_my_comments, name='dashboard_my_comments'),
    path('dashboard/delete/<int:num>', dashboard_delete, name='dashboard_delete'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

