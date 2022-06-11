from csv import reader
from dataclasses import dataclass
from urllib.request import Request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import admin
from .models import Usuarios, Adm_Usuarios, academia_adm, acesso_cliente
import datetime
from django.contrib import auth
# Create your views here.

def sessao_ativa(request):
    if request.user.is_authenticated:
        return True
    else:
        return False

def novo_usuario(request):
    if not sessao_ativa(request):
        return redirect('login')

    if request.user.is_admin is not True:
        raise PermissionError('Usuário atual não possui permissão para criar novos usuários')
    
    return render(request, 'Cliente/novo_usuario.html')

def criar_usuario(request):
    if not sessao_ativa(request):
        return redirect('login')

    if request.method == 'POST':
        
        username = request.POST['usuario_cadastro'] 
        email = request.POST['email_cadastro']
        password = request.POST['senha_cadastro']

        if request.user.is_superuser is True:
            user = academia_adm.objects.create_user(
            username = username,
            email = email, 
            password = password,
            is_staff = False,
            is_superuser = False,
            is_admin = True
        )
        elif request.user.is_admin is True:
            user = academia_adm.objects.create_user(
            username = username,
            email = email, 
            password = password,
            is_staff = False,
            is_superuser = False,
            is_admin = False
        )

        user.save()
        return redirect('menu')

def login(request):
    if request.method == 'POST':
        email = request.POST['login_acesso']
        senha = request.POST['senha_acesso']
        
        usuario = auth.authenticate(request, email=email, password=senha)

        if usuario is not None:
            auth.login(request, usuario)
            return redirect('menu')

    return render (request, 'Cliente/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def menu(request):
    if not sessao_ativa(request):
        return redirect('login')

    return render (request, 'Cliente/menu.html')

def clientes(request):
    if not sessao_ativa(request):
        return redirect('login')

    cliente = Usuarios.objects.all().order_by('-data_inicio')
    return render (request, 'Cliente/clientes.html', {'usuario': cliente})

def cadastro(request):
    if not sessao_ativa(request):
        return redirect('login')
    
    return render(request, 'Cliente/cadastro.html')

def acesso(request):
    if not sessao_ativa(request):
        return redirect('login')
    
    cliente = acesso_cliente.objects.all().order_by('-data_acesso')
    return render (request, 'Cliente/acesso.html', {'usuario': cliente})

def novo_acesso(request):
    if not sessao_ativa(request):
        return redirect('login')
    
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
    if not sessao_ativa(request):
        return redirect('login')
    
    if request.method == 'POST':
        nome = request.POST['nome']
        tel = request.POST['telefone']
        cpf_cliente = request.POST['cpf']
        valida_cpf = cpf_validate(cpf_cliente)
        
        try:
            cpf = int(''.join(i for i in cpf_cliente if i.isdigit()))
        except Exception as err:
            raise ValueError('CPF Inválido ou inexistente')

        data = request.POST['data_final']
        plano = request.POST['plano']
        quantidade_aulas = request.POST['quantidade_aulas']
        acesso_anterior = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
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
                data_inicio = datetime.datetime.now().strftime("%d/%m/%Y"),
                data_final = data,
                plano_escolhido = plano,
                quantidade_aulas = quantidade_aulas,
                acesso_anterior = acesso_anterior
            )
            cadastro.save()
            return redirect('menu')

    else:
        return render(request, 'Cliente/cadastro.html')

def realizar_acesso(request):
    if not sessao_ativa(request):
        return redirect('login')
    
    if request.method == 'POST':
        nome_acesso = ''
        cpf_acesso = request.POST['cpf_acesso']
        valida_cpf = cpf_validate(cpf_acesso)
        data_acesso = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
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

            return redirect('menu')
    else:
        return render(request, 'Cliente/novo_acesso.html')

def deletar_cliente(request):
    if not sessao_ativa(request):
        return redirect('login')
    
    if request.method == 'POST':
        id_deletar = request.POST['id_deletar']
        delete = Adm_Usuarios.deletar_cliente(
            id_usuario = id_deletar
        )
                
        return redirect('clientes')