from time import sleep
from django.shortcuts import render, redirect
from .models import Adm_Planos, Planos
# Create your views here.

def sessao_ativa(request):
    if request.user.is_authenticated:
        return True
    else:
        return False

def planos(request):
    if not sessao_ativa(request):
        return redirect('login')
    
    plano = Planos.objects.all().order_by('nome_plano')
    
    for c in plano:
        alunos = Adm_Planos().count_aluno(c)

    return render (request, 'Plano/planos.html', {'plano': plano})

def novo_plano(request):
    if not sessao_ativa(request):
        return redirect('login')
    try:
        edita_plano = request.POST['plano_editar_id']
        plano = Planos.objects.get(pk=edita_plano)
        return render(request, 'Plano/novo_plano.html', {'plano':plano})

    except Exception as err:
        return render(request, 'Plano/novo_plano.html')

def criar_plano(request):
    if not sessao_ativa(request):
        return redirect('login')
    
    if request.method == 'POST':
        nome_plano = str(request.POST['nome_do_plano']).title()

        try:
            quantidade_aulas = int(request.POST['qtd_aulas'])
            valor = int(request.POST['Valor'])
        except Exception as err:
            raise ValueError('Valor ou quantidade de aulas inválido')

        cadastro = Planos.objects.criar_plano(
            nome_plano = nome_plano,
            quantidade_aulas = quantidade_aulas,
            valor = valor,
        )
        cadastro.save()
        return redirect('menu')
    else:
        return render(request, 'Cliente/planos.html')

def editar_plano(request):
    if not sessao_ativa(request):
        return redirect('login')
    
    if request.method == 'POST':
        plano_id = request.POST['edito_plano']
        plano = Planos.objects.get(pk=plano_id)
        plano.nome_plano = request.POST['plano_editar']
        plano.quantidade_aulas = request.POST['qtd_plano_editar']
        plano.valor = request.POST['valor_editar']

        plano.nome_plano = str(request.POST['plano_editar']).title()

        try:
            plano.quantidade_aulas = int(request.POST['qtd_plano_editar'])
            plano.valor = int(request.POST['valor_editar'])
        except Exception as err:
            raise ValueError('Valor ou quantidade de aulas inválido')

        if not plano.nome_plano:
            raise ValueError('Plano precisa ter um nome')
        if not plano.quantidade_aulas:
            raise ValueError('Necessário quantidade de aulas')
        if not plano.valor:
            raise ValueError('Necessário valor')

        plano.save()
        return redirect('menu')
    else:
        return render(request, 'Cliente/planos.html')
    
def deletar_plano(request):
    if not sessao_ativa(request):
        return redirect('login')
    
    if request.method == 'POST':
        id_deletar = request.POST['id_delete_plano']
        usuario = Planos.objects.get(pk=id_deletar)
        usuario.delete()
                
        return redirect('planos')