from csv import reader
from dataclasses import dataclass
import time
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import admin
from .models import Usuarios, Adm_Usuarios, acesso_cliente
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

def acesso(request):
    cliente = acesso_cliente.objects.all().order_by('-data_acesso')
    return render (request, 'Cliente/acesso.html', {'usuario': cliente})

def novo_acesso(request):
    return render(request, 'Cliente/novo_acesso.html')

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
        cpf = int(''.join(i for i in cpf_cliente if i.isdigit()))
        data = request.POST['data_final']
        plano = request.POST['plano']
        quantidade_aulas = request.POST['quantidade_aulas']
        acesso_anterior = datetime.datetime.now()
        try:
            cpf = int(''.join(i for i in cpf_cliente if i.isdigit()))
        except Exception as err:
            raise ValueError('CPF Inválido ou inexistente')
        if valida_cpf == False:
            raise ValueError('CPF Inválido ou inexistente')
        else:
            cadastro = Usuarios.objects.criar_cliente(
                nome_completo = nome,
                telefone = tel,
                cpf = cpf,
                data_inicio = datetime.datetime.now(),
                data_final = data,
                plano_escolhido = plano,
                quantidade_aulas = quantidade_aulas,
                acesso_anterior = acesso_anterior
            )
            cadastro.save()
            return redirect('cadastro')
    else:
        return render(request, 'Cliente/cadastro.html')

def realizar_acesso(request):
    if request.method == 'POST':
        nome_acesso = ''
        cpf_acesso = request.POST['cpf_acesso']
        valida_cpf = cpf_validate(cpf_acesso)
        data_acesso = datetime.datetime.now()
        status_acesso = ''
        try:
            cpf = int(''.join(i for i in cpf_acesso if i.isdigit()))
        except Exception as err:
            raise ValueError('CPF Inválido ou inexistente')
        if valida_cpf == False:
            raise ValueError('CPF Inválido ou inexistente')
        else:
            cadastro = acesso_cliente.objects.criar_acesso(
                nome_acesso = nome_acesso,
                cpf_acesso = cpf,
                data_acesso = data_acesso,
                status_acesso = status_acesso
            )
            cadastro.save()

            contagem = acesso_cliente.objects.contagem_acesso(
                cpf = cpf,
                acesso_anterior = data_acesso
            )

            return redirect('novo_acesso')
    else:
        return render(request, 'Cliente/novo_acesso.html')