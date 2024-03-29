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
from .views import *


urlpatterns = [
    path('planos', planos, name='planos'),
    path('novo_plano', novo_plano, name='novo_plano'),
    path('criar_plano', criar_plano, name='criar_plano'),
    path('editar_plano', editar_plano, name='editar_plano'),
    path('deletar_plano', deletar_plano, name='deletar_plano')
]
