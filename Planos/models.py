from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import connection

# Create your models here.
class Adm_Planos(BaseUserManager):

    def criar_plano(self,nome_plano, quantidade_aulas, valor):
        try:
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
        except Exception as err:
            raise ValueError('Nome de plano não pode ser repetido')
    
    def count_aluno(self, nome_plano):

        cursor = connection.cursor()
        query = cursor.execute ('''select count(*) from Cliente_usuarios
        where plano_escolhido = "{}" '''.format(nome_plano))
        retorno = str(cursor.fetchone()[0])
        # print(retorno)

        for c in retorno:
            # print(retorno)
            query = cursor.execute('''update Planos_planos 
            set count_aluno = {} where nome_plano = '{}';'''.format(c, nome_plano))

    def aluno_ativo(self, nome_plano):

        cursor = connection.cursor()
        query = cursor.execute ('''select count(*) from Cliente_usuarios
        where plano_escolhido = "{}" and quantidade_aulas != 0; '''.format(nome_plano))
        retorno = str(cursor.fetchone()[0])
        # print(retorno)

        for c in retorno:
            # print(retorno)
            query = cursor.execute('''update Planos_planos 
            set alunos_ativos = {} where nome_plano = '{}';'''.format(c, nome_plano))


class Planos(models.Model):
    nome_plano = models.CharField(max_length=255, unique=True)
    quantidade_aulas = models.IntegerField()
    valor = models.IntegerField()
    count_aluno = models.IntegerField(default=0)
    alunos_ativos = models.IntegerField(default=0)

    data_criado = models.DateTimeField(auto_now_add=True)
    data_editado = models.DateTimeField(auto_now_add=True)

    objects = Adm_Planos()

    def __str__(self):
        return self.nome_plano
