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
from django.urls import path
from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.test),
    path("pos/", views.pos),
    path('index/', views.index),
    path('accounts/login/', views.login),
    path('accounts/logout/', views.logout),
    path('accounts/profile/', views.index),
    path('accounts/register/', views.register),
    path('customizationform/', views.CustomizationForm),
    path('perchaselist/', views.perchaselist),
    path('purchasepostform/', views.purchasepostform),
    path('delete/<int:id>', views.delete),
    path('edit/<int:id>/', views.edit),
    path('herbstocklist/',views.herbstocklist),
    path('salelist/',views.salelist)
]
