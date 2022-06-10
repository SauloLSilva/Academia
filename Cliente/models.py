from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import sqlite3
import datetime
# Create your models here.

class Adm_Usuarios(BaseUserManager):
    
    def criar_cliente(self, nome_completo, telefone, cpf, data_inicio, data_final, plano_escolhido,quantidade_aulas, acesso_anterior):
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
            quantidade_aulas = quantidade_aulas,
            acesso_anterior = acesso_anterior
        )
        cliente.save(using=self._db)
    
        return cliente

    def criar_acesso(self, nome_acesso, cpf_acesso, data_acesso, status_acesso):
        # if not nome_acesso:
        #     raise ValueError('Usuario precisa ter um nome completo')
        if not cpf_acesso:
            raise ValueError('Necessário CPF')

        conectar = sqlite3.connect('academiaDjango.db')
        cursor = conectar.cursor()
        query = cursor.execute('''select * from Cliente_usuarios 
        where cpf == {}'''.format(cpf_acesso))

        try:
            retorno = (query.fetchone())
            aluno = retorno[3]
            qtd_aulas = int(retorno[12])

            if qtd_aulas !=0:

                cliente = self.model(
                    nome_acesso = aluno,
                    cpf_acesso = cpf_acesso,
                    data_acesso = data_acesso,
                    status_acesso = 'Liberado',
                )
                cliente.save(using=self._db)
        
                return cliente
            else:
                cliente = self.model(
                    nome_acesso = aluno,
                    cpf_acesso = cpf_acesso,
                    data_acesso = data_acesso,
                    status_acesso = 'Bloqueado',
                )
                cliente.save(using=self._db)
        
                return cliente
        except Exception as err:
            raise ValueError('CPF não encontrado')

    def deletar_cliente(id_usuario):
        conectar = sqlite3.connect('academiaDjango.db')
        cursor = conectar.cursor()
        query = cursor.execute('''DELETE FROM Cliente_usuarios Where id = {}'''.format(id_usuario))
        conectar.commit()
        conectar.close()

    
    def contagem_acesso(self, cpf, acesso_anterior):
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
            # conectar.close()
            
            query2 = cursor.execute('''update Cliente_usuarios 
            set acesso_anterior = '{}' 
            where cpf == {};'''.format(acesso_anterior,cpf))
            conectar.commit()
            conectar.close()

        elif qtd_restante == 1:
            query = cursor.execute('''update Cliente_usuarios 
            set quantidade_aulas = quantidade_aulas - 1 
            where cpf == {};'''.format(cpf))
            conectar.commit()
            # conectar.close()
            
            query2 = cursor.execute('''update Cliente_usuarios 
            set acesso_anterior = '{}' 
            where cpf == {};'''.format(acesso_anterior,cpf))
            conectar.commit()
            conectar.close()
            raise ValueError('Cliente fez última aula contratada, atualizar plano')
        
        elif qtd_restante == 0:
            raise ValueError ('Cliente fez todas as aulas ou não renovou plano')
        
        else:
            raise ValueError('CPF não encontrado')

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Usuario deve ter um endereço de email")

        usuario = self.model(
            email=self.normalize_email(email)
        )

        usuario.set_password(password)
        usuario.save(using=self._db)

        return usuario

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("Usuario deve ter um endereço de email")

        usuario = self.model(
            email=self.normalize_email(email),
            is_staff = True,
            is_superuser = True,
            is_admin = True

        )

        usuario.set_password(password)
        usuario.save(using=self._db)

        return usuario


class Usuarios(AbstractBaseUser):
    nome_completo = models.CharField(max_length=255)
    telefone = models.CharField(max_length=11)
    cpf = models.CharField(max_length=13)
    data_inicio = models.CharField(max_length=30)
    data_final = models.CharField(max_length=30)
    plano_escolhido = models.CharField(max_length=50)
    quantidade_aulas = models.CharField(max_length=3)
    acesso_anterior = models.CharField(max_length=30)

    
    data_criado = models.CharField(max_length=30)
    data_editado = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['nome_completo','plano_escolhido', 'cpf', 'quantidade_aulas']
    USERNAME_FIELD = 'nome_completo'

    objects = Adm_Usuarios()

    def __str__(self):
        return self.nome_completo

class acesso_cliente(AbstractBaseUser):
    nome_acesso = models.CharField(max_length=255)
    cpf_acesso = models.CharField(max_length=13)
    data_acesso = models.CharField(max_length=30)
    status_acesso = models.CharField(max_length=13)

    REQUIRED_FIELDS = ['nome_acesso','cpf_acesso', 'data_acesso', 'status_acesso']
    USERNAME_FIELD = 'nome_acesso'

    objects = Adm_Usuarios()
    
    def __str__(self):
        return self.nome_acesso

class academia_adm(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    # username = models.CharField(max_length=30, unique=True)
    
    data_criado = models.CharField(max_length=30)
    data_editado = models.CharField(max_length=30)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    # has_module_perms = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'

    objects = Adm_Usuarios()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
