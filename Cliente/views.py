from csv import reader
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import admin
from .models import Usuarios, Adm_Usuarios
import datetime
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

def cpf_validate(numbers):
    #  Obtém os números do CPF e ignora outros caracteres
    cpf = [int(char) for char in numbers if char.isdigit()]

    #  Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
    #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
    #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
    if cpf == cpf[::-1]:
        return False

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True

def realizar_cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        tel = request.POST['telefone']
        cpf_cliente = request.POST['cpf']
        valida_cpf = cpf_validate(cpf_cliente)
        data = request.POST['data_final']
        plano = request.POST['plano']
        if valida_cpf == False:
            raise ValueError('CPF Inválido ou inexistente')
        else:
            cadastro = Usuarios.objects.criar_cliente(
                nome_completo = nome,
                telefone = tel,
                cpf = cpf_cliente,
                data_inicio = datetime.datetime.now(),
                data_final = data,
                plano_escolhido = plano
            )
            cadastro.save()
            return redirect('cadastro')
    else:
        return render(request, 'Cliente/cadastro.html')