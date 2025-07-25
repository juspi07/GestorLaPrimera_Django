"""
URL configuration for Gestor_LaPrimeraDjango project.

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
from mysite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('facturador/', views.facturador, name='facturador'),
    path('buscar_clientes/', views.buscar_clientes, name='buscar_clientes'),
    path('seleccionar_cliente/', views.select_cliente, name='select_clientes'),
    path('buscar_productos/', views.buscar_productos, name='buscar_productos'),
    path('conectar/', views.conectar_Afip, name='conectar'),
    path('conectar-wsaa/', views.conectar_wsaa, name='conectar_wsaa'),
]
