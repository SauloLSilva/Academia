from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import sqlite3
from django.db import connection

# Create your models here.

class Adm_Usuarios(BaseUserManager):
    
    def criar_cliente(self, nome_completo, telefone, cpf, data_inicio, data_final, plano_escolhido,quantidade_aulas, acesso_anterior):
        if not nome_completo:
            raise ValueError('Usuario precisa ter um nome completo')
        if not plano_escolhido:
            raise ValueError('Usuário não possui plano indicado')
        if not quantidade_aulas:
            raise ValueError('Usuário sem quantidade de aulas definida')

        try:
            cursor = connection.cursor()
            query = cursor.execute("""select * from Cliente_usuarios 
            where cpf = {} and plano_escolhido = '{}'; """.format(cpf, plano_escolhido))
            retorno = list(str(cursor.fetchall()).split(','))
            plano_cadastrado = (retorno[8][2:-1])

            if plano_escolhido == plano_cadastrado:
                raise ValueError('Cliente já cadastrado nesse plano')
            else:
            
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
        except IndexError:

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

    def criar_acesso(self, plano_acesso, nome_acesso, cpf_acesso, data_acesso, status_acesso):
        if not cpf_acesso:
            raise ValueError('Necessário CPF')

        cursor = connection.cursor()
        query = cursor.execute("""select * from Cliente_usuarios
        where cpf = {} and plano_escolhido = '{}'""".format(cpf_acesso, plano_acesso))

        try:
            retorno = list(str(cursor.fetchall()).split(','))
            aluno = (retorno[3][2:-1])
            print(aluno)
            qtd_aulas = int(retorno[12])

            if qtd_aulas !=0:

                cliente = self.model(
                    nome_acesso = aluno,
                    plano_acesso = plano_acesso,
                    cpf_acesso = cpf_acesso,
                    data_acesso = data_acesso,
                    status_acesso = 'Liberado',
                )
                cliente.save(using=self._db)
        
                return cliente
            else:
                cliente = self.model(
                    nome_acesso = aluno,
                    plano_acesso = plano_acesso,
                    cpf_acesso = cpf_acesso,
                    data_acesso = data_acesso,
                    status_acesso = 'Bloqueado',
                )
                cliente.save(using=self._db)
        
                return cliente
        except Exception as err:
            print(err)
            raise ValueError('CPF não encontrado ou não cadastrado nesse plano')

    
    def contagem_acesso(self, cpf, acesso_anterior, plano):
        cursor = connection.cursor()
        query = cursor.execute("""select * from Cliente_usuarios 
        where cpf = {};""".format(cpf))

        retorno = list(str(cursor.fetchall()).split(','))
        qtd_restante = int(retorno[12])
        
        if retorno != None and 'None' and qtd_restante >= 2:
            query = cursor.execute("""update Cliente_usuarios 
            set quantidade_aulas = quantidade_aulas - 1 
            where cpf = {} and plano_escolhido = '{}';""".format(cpf, plano))
            
            query2 = cursor.execute("""update Cliente_usuarios 
            set acesso_anterior = '{}' 
            where cpf = {} and plano_escolhido = '{}';""".format(acesso_anterior, cpf, plano))

        elif qtd_restante == 1:
            query = cursor.execute("""update Cliente_usuarios 
            set quantidade_aulas = quantidade_aulas - 1 
            where cpf = {} and plano_escolhido = '{}';""".format(cpf, plano))
            
            query2 = cursor.execute("""update Cliente_usuarios 
            set acesso_anterior = '{}' 
            where cpf = {} and plano_escolhido = '{}';""".format(acesso_anterior, cpf, plano))
            raise ValueError('Cliente fez última aula contratada, atualizar plano')
        
        elif qtd_restante == 0:
            raise ValueError ('Cliente fez todas as aulas ou não renovou plano')
        
        else:
            raise ValueError('CPF não encontrado')

    def create_user(self, username, email, is_admin, is_superuser, is_staff, password=None):
        if not email:
            raise ValueError("Usuario deve ter um endereço de email")
        if not password:
            raise ValueError("Usuario deve ter uma senha")
        if not username:
            raise ValueError("Usuario deve ter um username único")

        try:
            usuario = self.model(
                username = username,
                email=self.normalize_email(email),
                is_admin = is_admin,
                is_active = True,
                is_superuser = is_superuser,
                is_staff = is_staff
            )

            usuario.set_password(password)
            usuario.save(using=self._db)

            return usuario
        except Exception as err:
            raise ValueError("Email já cadastrado, inválido ou tentativa de cadastro sem senha")

    def create_superuser(self,username ,email, password=None):
        if not email:
            raise ValueError("Usuario deve ter um endereço de email")
        if not password:
            raise ValueError("Usuario deve ter uma senha")
        if not username:
            raise ValueError("Usuario deve ter um username único")

        usuario = self.model(
            username = username,
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
    quantidade_aulas = models.IntegerField()
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
    plano_acesso = models.CharField(max_length=13)
    data_acesso = models.CharField(max_length=30)
    status_acesso = models.CharField(max_length=13)

    REQUIRED_FIELDS = ['nome_acesso','cpf_acesso', 'data_acesso', 'status_acesso']
    USERNAME_FIELD = 'nome_acesso'

    objects = Adm_Usuarios()
    
    def __str__(self):
        return self.nome_acesso

class academia_adm(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    
    data_criado = models.CharField(max_length=30)
    data_editado = models.CharField(max_length=30)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    objects = Adm_Usuarios()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
