from django.shortcuts import render

# Create your views here.

def planos(request):
    return render (request, 'Plano/planos.html')