"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from my_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.render_items, name='render_items'),
    path('card/', views.open_card),
    path('basket/', views.render_basket),
    path('add_to_basket/<int:item_id>/', views.add_to_basket, name='add_to_basket'),
    path('delete_from_basket/<int:item_id>/', views.delete_from_basket, name='delete_from_basket'),
]
