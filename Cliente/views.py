from csv import reader
from dataclasses import dataclass
from urllib.request import Request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import admin
from .models import Usuarios, Adm_Usuarios, academia_adm, acesso_cliente
from Planos.models import Planos
import datetime
from django.contrib import auth
from django.db import connection
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

    try:
        editar_cliente = request.POST['id_editar_cliente']
        cliente = Usuarios.objects.get(pk=editar_cliente)
        plano = Planos.objects.all()

        return render(request,'Cliente/cadastro.html', {'usuario': cliente, 'plano': plano})
    except Exception as err:
        plano = Planos.objects.all()
    
        return render(request, 'Cliente/cadastro.html', {'plano':plano})

def acesso(request):
    if not sessao_ativa(request):
        return redirect('login')
    
    cliente = acesso_cliente.objects.all().order_by('-data_acesso')
    return render (request, 'Cliente/acesso.html', {'usuario': cliente})

def novo_acesso(request):
    if not sessao_ativa(request):
        return redirect('login')

    plano = Planos.objects.all()
    
    return render(request, 'Cliente/novo_acesso.html', {'plano':plano})

def cpf_validate(numbers):
    cpf = [int(char) for char in numbers if char.isdigit()]

    if len(cpf) != 11:
        return False

    if cpf == cpf[::-1]:
        return False

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
        try:
            quantidade_aulas = int(request.POST['quantidade_aulas'])
        except Exception as err:
            raise ValueError('Quantidade de aulas inválida')
            
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

def editar_cadastro(request):
    if not sessao_ativa(request):
        return redirect('login')
    
    if request.method == 'POST':
        editar_cliente = request.POST['editar_id']
        cliente = Usuarios.objects.get(pk=editar_cliente)
        plano_cadastrado_editar = cliente.plano_escolhido
        cliente.nome_completo = request.POST['nome_editar']
        cliente.telefone = request.POST['telefone_editar']
        cpf_cliente = request.POST['cpf_editar']
        valida_cpf = cpf_validate(cpf_cliente)

        try:
            cpf = int(''.join(i for i in cpf_cliente if i.isdigit()))
        except Exception as err:
            raise ValueError('CPF Inválido ou inexistente')

        cliente.data_inicio = request.POST['data_matricula_editar']
        cliente.data_final = request.POST['data_final_editar']
        cliente.plano_escolhido = request.POST['plano_editar']
        try:
            cliente.quantidade_aulas = int(request.POST['quantidade_aulas_editar'])
        except Exception as err:
            raise ValueError('Quantidade de aulas inválida')
            
        try:
            cliente.cpf = int(''.join(i for i in cpf_cliente if i.isdigit()))
        except Exception as err:
            raise ValueError('CPF Inválido ou inexistente')
        if valida_cpf == False:
            raise ValueError('CPF Inválido ou inexistente')

        if not cliente.nome_completo:
            raise ValueError('Usuario precisa ter um nome completo')
        if not cliente.plano_escolhido:
            raise ValueError('Usuário não possui plano indicado')
        if not cliente.quantidade_aulas:
            raise ValueError('Usuário sem quantidade de aulas definida')

        try:
            if cliente.plano_escolhido == plano_cadastrado_editar:
                cliente.save()
                return redirect('clientes')

            else:
                cursor = connection.cursor()
                query = cursor.execute("""select * from Cliente_usuarios 
                    where cpf = {} and plano_escolhido = '{}'; """.format(cpf, cliente.plano_escolhido))
                retorno = list(str(cursor.fetchall()).split(','))
                plano_cadastrado = (retorno[8][2:-1])

                if cliente.plano_escolhido == plano_cadastrado:
                    raise ValueError('Cliente já cadastrado nesse plano')
                else:

                    cliente.save()
                    return redirect('clientes')
        except IndexError:
            cliente.save()
            return redirect('clientes')

    else:
        return render(request, 'Cliente/cadastro.html')

def realizar_acesso(request):
    if not sessao_ativa(request):
        return redirect('login')
    
    if request.method == 'POST':
        nome_acesso = ''
        cpf_acesso = request.POST['cpf_acesso']
        plano_acesso = request.POST['plano_acesso']
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
                plano_acesso = plano_acesso,
                data_acesso = data_acesso,
                status_acesso = status_acesso
            )

            cadastro.save()

            contagem = acesso_cliente.objects.contagem_acesso(
                cpf = cpf,
                plano = plano_acesso,
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
        usuario = Usuarios.objects.get(pk=id_deletar)
        usuario.delete()
                
        return redirect('clientes')