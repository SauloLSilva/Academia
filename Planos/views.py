from django.shortcuts import render
from .models import Planos
# Create your views here.

def planos(request):
    plano = Planos.objects.all()
    return render (request, 'Plano/planos.html', {'plano': plano})