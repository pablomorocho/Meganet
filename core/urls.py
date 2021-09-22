"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView,PasswordChangeDoneView,PasswordResetCompleteView,PasswordChangeView,PasswordResetDoneView
from django.urls import path
from home import views
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'password_reset_done/',
        PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),name='password_reset_confirm'
    ),
    path('', views.index ,name="index"),
    path('logout/', views.logout ,name="logout"),
    
    #empresas
    path('inicio/', views.inicio,name="inicio"),
    path('nueva-empresa/', views.nueva_empresa,name="nueva-empresa"),
    path('editar-empresa/<id>', views.editar_empresa,name="editar-empresa"),
    path('eliminar-empresa/<id>', views.eliminar_empresa,name="eliminar-empresa"),
  
    #agencias
    path('agencias/', views.agencias,name="agencias"),
    path('nueva-agencia/', views.nueva_agencia,name="nueva-agencia"),
    path('editar-agencia/<id>', views.editar_agencia,name="editar-agencia"),
    path('eliminar-agencia/<id>', views.eliminar_agencia,name="eliminar-agencia"),
    
    
    #planes
    path('planes/', views.planes,name="planes"),
    path('nuevo-plan/', views.nuevo_plan,name="nueva-plan"),
    path('editar-plan/<id>', views.editar_plan,name="editar-plan"),
    path('eliminar-plan/<id>', views.eliminar_plan,name="eliminar-plan"),
    
    #secretaria(o)s
    path('secretarias/', views.secretarias,name="secretarias"),
    path('nueva-secretaria/', views.nueva_secretaria,name="nueva-secretaria"),
    path('editar-secretaria/<id>', views.editar_secretaria,name="editar-secretaria"),
    path('eliminar-secretaria/<id>', views.eliminar_secretaria,name="eliminar-secretaria"),
    
    #tecnicos
    path('tecnicos/', views.tecnicos,name="tecnicos"),
    path('nuevo-tecnico/', views.nuevo_tecnico,name="nuevo-tecnico"),
    path('editar-tecnico/<id>', views.editar_tecnico,name="editar-tecnico"),
    path('eliminar-tecnico/<id>', views.eliminar_tecnico,name="eliminar-tecnico"),
    
    
    #clientes
    path('clientes/', views.clientes,name="clientes"),
    path('nuevo-cliente/', views.nuevo_cliente,name="nuevo-cliente"),
    path('editar-cliente/<id>', views.editar_cliente,name="editar-cliente"),
    path('eliminar-cliente/<id>', views.eliminar_cliente,name="eliminar-cliente"),
    
    
    #contratos
    path('contratos/', views.contratos,name="contratos"),
    path('nuevo-contrato/', views.nuevo_contrato,name="nuevo-contrato"),
    path('editar-contrato/<id>', views.editar_contrato,name="editar-contrato"),
    path('eliminar-contrato/<id>', views.eliminar_contrato,name="eliminar-contrato"),


    #agendamientos
    path('agendamientos/', views.agendamientos,name="agendamientos"),
    url(r'^nuevo-agendamiento/$', views.nuevo_agendamiento, name='nuevo-agendamiento'),
  
    path('editar-agendamiento/<id>', views.editar_agendamiento,name="editar-agendamiento"),
    path('eliminar-agendamiento/<id>', views.eliminar_agendamiento,name="eliminar-agendamiento"),


    #pagos
    path('registro-pagos/', views.registo_pagos,name="registro-pagos"),
    url(r'^nuevo-pago/$', views.nuevo_pago, name='nuevo-pago'),  
    path('editar-pago/<id>', views.editar_pago,name="editar-pago"),
    path('eliminar-pago/<id>', views.eliminar_pago,name="eliminar-pago"),


    path('obtener_datos/', views.obtener_datos, name='obtener_datos'),

    path('change-password/<id>', views.cambiarContraseña,name="change-password"),
]
