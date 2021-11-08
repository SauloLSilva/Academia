from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.

def clientes(request):
    return render (request, 'clientes.html')
    
def login(request):
    return render (request, 'login.html')

def menu(request):
    return render (request, 'menu.html')

def cadastro(request):
    return render(request, 'cadastro.html')