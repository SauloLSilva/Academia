from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import admin
from .models import Usuarios

# Create your views here.

def clientes(request):
    cliente = Usuarios.objects.all().order_by('-data_inicio')
    return render (request, 'Cliente/clientes.html', {'usuario': cliente})
    
def login(request):
    return render (request, 'Cliente/login.html')

def menu(request):
    return render (request, 'Cliente/menu.html')

def cadastro(request):
    return render(request, 'Cliente/cadastro.html')