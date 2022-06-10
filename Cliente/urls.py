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
from django.urls import path
from .views import *


urlpatterns = [
    path('clientes', clientes, name='clientes'),
    path('', login, name='login'),
    path('menu', menu, name='menu'),
    path('cadastro', cadastro, name='cadastro'),
    path('acesso', acesso, name='acesso'),
    path('novo_acesso', novo_acesso, name='novo_acesso'),
    path('realizar_cadastro', realizar_cadastro, name='realizar_cadastro'),
    path('realizar_acesso', realizar_acesso, name='realizar_acesso'),
    path('deletar_cliente', deletar_cliente, name='deletar_cliente'),
    path('logout', logout, name='logout')
]
