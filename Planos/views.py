from django.shortcuts import render, redirect
from .models import Planos
# Create your views here.

def planos(request):
    plano = Planos.objects.all()
    return render (request, 'Plano/planos.html', {'plano': plano})

def novo_plano(request):
    return render(request, 'Plano/novo_plano.html')

def criar_plano(request):
    if request.method == 'POST':
        nome_plano = request.POST['nome_do_plano']
        quantidade_aulas = request.POST['qtd_aulas']
        valor = request.POST['Valor']
        cadastro = Planos.objects.criar_plano(
            nome_plano = nome_plano,
            quantidade_aulas = quantidade_aulas,
            valor = valor,
        )
        cadastro.save()
        return redirect('novo_plano')
    else:
        return render(request, 'Cliente/planos.html')