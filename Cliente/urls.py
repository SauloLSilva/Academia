"""AcademiaDjango URL Configuration

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
# Adcionar url de menu do site
from django.contrib import admin
from django.urls import path
from Cliente import views


urlpatterns = [
    path('clientes', views.clientes, name='clientes'),
    path('', views.login, name='login'),
    path('menu', views.menu, name='menu'),
    path('cadastro', views.cadastro, name='cadastro')
    # path('editar_cliente', editar_cliente, name=editar_cliente),
    # path('cadastrar_cliente', cadastrar_cliente, name=cadastrar_cliente),
    # path('deletar_cliente', deletar_cliente, name= deletar_cliente),

    # path('login', login, name=login),
    # path('logout', logout, name=logout),
]
