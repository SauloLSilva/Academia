# Academia

Projeto de framework api desenvolvida em Django e OS Linux

# antes de instalar requirements

instalar pip: sudo apt install piṕ
para instalação de django: pip install django

# instalar requirements (necessário para operação correta do projeto)
sudo pip3 install -r requirements_linux.txt

# para coletar dados de static usar
python3 manage.py collectstatic

# para abrir banco
sudo apt install sqlite

# para visualizar banco de forma externa

utlilizar DB Browser: sudo apt-get install sqlitebrowser

# para rodar projeto

python3 manage.py migrate
python3 manage.py runserver
