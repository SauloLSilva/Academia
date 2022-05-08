from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import sqlite3
# Create your models here.

class Adm_Usuarios(BaseUserManager):
    
    def criar_cliente(self, nome_completo, telefone, cpf, data_inicio, data_final, plano_escolhido,quantidade_aulas):
        if not nome_completo:
            raise ValueError('Usuario precisa ter um nome completo')
        if not plano_escolhido:
            raise ValueError('Usuário não possui plano indicado')
        if not quantidade_aulas:
            raise ValueError('Usuário sem quantidade de aulas definida')

        cliente = self.model(
            nome_completo = nome_completo,
            telefone = telefone,
            cpf = cpf,
            data_inicio = data_inicio,
            data_final = data_final,
            plano_escolhido = plano_escolhido,
            quantidade_aulas = quantidade_aulas
        )
        cliente.save(using=self._db)
    
        return cliente

    def criar_acesso(self, nome_acesso, cpf_acesso, data_acesso):
        if not nome_acesso:
            raise ValueError('Usuario precisa ter um nome completo')
        if not cpf_acesso:
            raise ValueError('Necessário CPF')

        cliente = self.model(
            nome_acesso = nome_acesso,
            cpf_acesso = cpf_acesso,
            data_acesso = data_acesso,
        )
        cliente.save(using=self._db)
    
        return cliente
    
    def contagem_acesso(self, cpf):
        conectar = sqlite3.connect('academiaDjango.db')
        cursor = conectar.cursor()
        query = cursor.execute('''select * from Cliente_usuarios 
        where cpf == {}'''.format(cpf))

        retorno = (query.fetchone())
        qtd_restante = int(retorno[12])
        
        if retorno != None and 'None' and qtd_restante >= 2:
            query = cursor.execute('''update Cliente_usuarios 
            set quantidade_aulas = quantidade_aulas - 1 
            where cpf == {};'''.format(cpf))
            conectar.commit()
            conectar.close()

        elif qtd_restante == 1:
            query = cursor.execute('''update Cliente_usuarios 
            set quantidade_aulas = quantidade_aulas - 1 
            where cpf == {};'''.format(cpf))
            conectar.commit()
            conectar.close()
            raise ValueError('Cliente fez última aula contratada, atualizar plano')
        
        elif qtd_restante == 0:
            raise ValueError ('Cliente fez todas as aulas ou não renovou plano')
        
        else:
            raise ValueError('CPF não encontrado')


class Usuarios(AbstractBaseUser):
    nome_completo = models.CharField(max_length=255)
    telefone = models.CharField(max_length=11)
    cpf = models.CharField(max_length=13)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_final = models.CharField(max_length=30)
    plano_escolhido = models.CharField(max_length=50)
    quantidade_aulas = models.CharField(max_length=3)

    
    data_criado = models.DateTimeField(auto_now_add=True)
    data_editado = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['nome_completo','plano_escolhido', 'cpf', 'quantidade_aulas']
    USERNAME_FIELD = 'nome_completo'

    objects = Adm_Usuarios()

    def __str__(self):
        return self.nome_completo

class acesso_cliente(AbstractBaseUser):
    nome_acesso = models.CharField(max_length=255)
    cpf_acesso = models.CharField(max_length=13)
    data_acesso = models.DateTimeField(max_length=30)

    REQUIRED_FIELDS = ['nome_acesso','cpf_acesso', 'data_acesso']
    USERNAME_FIELD = 'nome_acesso'

    objects = Adm_Usuarios()
    
    def __str__(self):
        return self.nome_acesso
