import os
import subprocess
from tqdm import tqdm

# Cria a pasta static se ainda não existir
if not os.path.isdir('/app/static'):
    with tqdm(desc='Criando pasta static', unit='passo') as progress:
        os.makedirs('/app/static')
        progress.update()

# Copia os arquivos do projeto para o diretório /app
with tqdm(desc='Copiando arquivos', unit='file') as progress:
    subprocess.run(['cp', '-r', '.', '/app'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    progress.update()

# Instala pacotes necessários
with tqdm(desc='Instalando requisitos', unit='package') as progress:
    subprocess.run(['pip', 'install', '--upgrade', 'pip'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    progress.update()
    subprocess.run(['pip', 'install', '-r', '/app/requirements.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    progress.update()

# Executa as migrações do banco de dados
with tqdm(desc='Migrando banco de dados', unit='step') as progress:
    os.chdir('/app')
    subprocess.run(['python', 'manage.py', 'migrate'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    progress.update()

# Coleta os arquivos estáticos do Django
with tqdm(desc='Coletando arquivos estáticos', unit='file') as progress:
    subprocess.run(['python', 'manage.py', 'collectstatic'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    progress.update()

# Inicia o servidor web Gunicorn
subprocess.run(['gunicorn', 'userApi.wsgi:application', '--bind', 'web:8000'])
