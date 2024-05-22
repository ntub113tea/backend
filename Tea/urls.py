"""Tea URL Configuration

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
from django.urls import path,include
from myapp import views
from django.contrib.auth import views as auth_views
from myapp.routing import websocket_urlpatterns  # 引用 WebSocket 路徑配置

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rgst/', views.rgst),
    path('index/', views.index),
    path('',views.url),
    path("manage/", views.manage),
    path('staff/',views.staff),
    path("pos/", views.pos),
    path('question/', views.question),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout),
    path('accounts/profile/', views.index),
    path('accounts/register/', views.register),
    path('perchaselist/', views.perchaselist),
    path('purchasepostform/', views.purchasepostform),
    path('delete/<int:id>', views.delete),
    path('edit/<int:id>/', views.edit),
    path('herbstocklist/',views.herbstocklist),
    path('salelist/',views.salelist,name='salelist'),
    path('salelist_staff/',views.salelist_staff,name='salelist'),
    path('check_inventory/', views.check_inventory),
    path('history/', views.history_view, name='history'),
    path('ws/', include(websocket_urlpatterns)),  # 包含 WebSocket 路徑
]


