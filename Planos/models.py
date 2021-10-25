from django.db import models

# Create your models here.

class Planos(models.Model):
    nome_plano = models.CharField(max_length=255)
    quantidade_aulas = models.CharField(max_length=3)
    valor = models.CharField(max_length=6)

    data_criado = models.DateTimeField(auto_now_add=True)
    data_editado = models.DateTimeField(auto_now_add=True)