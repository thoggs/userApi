import os
from tqdm import tqdm


# Define uma função auxiliar para executar um comando com barras de progresso
def run_with_progress(command, desc):
    with tqdm(desc=desc, unit="") as progress:
        for line in os.popen(command):
            progress.update()


# Cria o ambiente virtual na pasta .venv
run_with_progress("python -m venv /app/.venv", "Criando ambiente virtual")

# Ativa o ambiente virtual
activate = "/app/.venv/bin/activate"
if os.path.isfile(activate):
    exec(open(activate).read(), {"__file__": activate})

# Define o caminho do sistema para o ambiente virtual
os.environ["PATH"] = "/app/.venv/bin:" + os.environ["PATH"]

# Cria a pasta static se ainda não existir
if not os.path.isdir("/app/static"):
    os.mkdir("/app/static")

# Copia os arquivos do projeto para o diretório /app
run_with_progress("cp -r . /app", "Copiando arquivos")

# Instala pacotes necessários
run_with_progress("pip install --upgrade pip && pip install -r /app/requirements.txt", "Instalando pacotes")

# Executa as migrações do banco de dados
run_with_progress("python manage.py migrate", "Executando migrações")

# Coleta os arquivos estáticos do Django
run_with_progress("python manage.py collectstatic", "Coletando arquivos estáticos")

# Inicia o servidor web Gunicorn
os.execlp("gunicorn", "gunicorn", "userApi.wsgi:application", "--bind", "web:8000")
