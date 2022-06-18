# Academia

Projeto de framework api desenvolvida em Django e OS Linux

# antes de instalar requirements

instalar pip: sudo apt install pip
para instalação de django: pip install django
instalar o MySql: pip install mysqlclient
para criar database:
mysql -u root -p (senha root)
create database academiaDjango;

# instalar requirements (necessário para operação correta do projeto)
sudo pip3 install -r requirements_linux.txt

# para coletar dados de static usar
python3 manage.py collectstatic

# para abrir banco
Usar o MySql workbench
modificar password em AcademiaDjango > settings para o password usado localmente

# para visualizar banco de forma externa

instalar o MySql workbench

# para rodar projeto

python3 manage.py migrate
python3 manage.py createsuperuser (ou não irá conseguir acessar interface)
python3 manage.py runserver
