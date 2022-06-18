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
    return render (request, 'Plano/planos.html', {'plano': plano})

def novo_plano(request):
    if not sessao_ativa(request):
        return redirect('login')
    
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
    
def deletar_plano(request):
    if not sessao_ativa(request):
        return redirect('login')
    
    if request.method == 'POST':
        id_deletar = request.POST['id_delete_plano']
        usuario = Planos.objects.get(pk=id_deletar)
        usuario.delete()
                
        return redirect('planos')