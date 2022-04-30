from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class Adm_Usuarios(BaseUserManager):
    
    def criar_cliente(self, nome_completo, telefone, cpf, data_inicio, data_final, plano_escolhido):
        if not nome_completo:
            raise ValueError('Usuario precisa ter um nome completo')
        if not plano_escolhido:
            raise ValueError('Usuário não possui plano indicado')

        cliente = self.model(
            nome_completo = nome_completo,
            telefone = telefone,
            cpf = cpf,
            data_inicio = data_inicio,
            data_final = data_final,
            plano_escolhido = plano_escolhido
        )
        cliente.save(using=self._db)
    
        return cliente

class Usuarios(AbstractBaseUser):
    nome_completo = models.CharField(max_length=255)
    telefone = models.CharField(max_length=11)
    cpf = models.CharField(max_length=13)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_final = models.CharField(max_length=30)
    plano_escolhido = models.CharField(max_length=50)
    
    data_criado = models.DateTimeField(auto_now_add=True)
    data_editado = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['nome_completo','plano_escolhido', 'cpf']
    USERNAME_FIELD = 'nome_completo'

    objects = Adm_Usuarios()

    def __str__(self):
        return self.nome_completo