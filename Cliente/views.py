from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.

def clientes(request):
    return render (request, 'Cliente/clientes.html')
    
def login(request):
    return render (request, 'Cliente/login.html')

def menu(request):
    return render (request, 'Cliente/menu.html')

def cadastro(request):
    return render(request, 'Cliente/cadastro.html')