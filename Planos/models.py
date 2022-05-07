from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class Adm_Planos(BaseUserManager):

    def criar_plano(self,nome_plano, quantidade_aulas, valor):
        if not nome_plano:
            raise ValueError('Plano precisa ter um nome')
        if not quantidade_aulas:
            raise ValueError('Necessário quantidade de aulas')
        if not valor:
            raise ValueError('Necessário valor')

        plano = self.model(
            nome_plano = nome_plano,
            quantidade_aulas = quantidade_aulas,
            valor = valor,
            )
        plano.save(using=self._db)
        
        return plano

class Planos(models.Model):
    nome_plano = models.CharField(max_length=255)
    quantidade_aulas = models.CharField(max_length=3)
    valor = models.CharField(max_length=6)

    data_criado = models.DateTimeField(auto_now_add=True)
    data_editado = models.DateTimeField(auto_now_add=True)

    objects = Adm_Planos()