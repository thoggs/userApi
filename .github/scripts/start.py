#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

from tqdm import tqdm


def run_command(cmd, desc):
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        for line in tqdm(iter(proc.stdout.readline, b''), desc=desc, unit='B', unit_scale=True):
            sys.stdout.write(line.decode('utf-8'))
            sys.stdout.flush()
        for line in tqdm(iter(proc.stderr.readline, b''), desc=desc, unit='B', unit_scale=True):
            sys.stdout.write(line.decode('utf-8'))
            sys.stdout.flush()
        proc.wait()


# Cria o ambiente virtual na pasta .venv
run_command(['python', '-m', 'venv', '/app/.venv'], 'Criando ambiente virtual')

# Ativa o ambiente virtual
run_command(['source', '/app/.venv/bin/activate'], 'Ativando ambiente virtual')

# Define o caminho do sistema para o ambiente virtual
run_command(['export', 'PATH="/app/.venv/bin:$PATH"'], 'Definindo caminho do sistema')

# Cria a pasta static se ainda não existir
static_dir = Path('/app/static')
if not static_dir.is_dir():
    static_dir.mkdir(parents=True)
    print(f"Criando pasta {static_dir}.")

# Copia os arquivos do projeto para o diretório /app
run_command(['cp', '-r', '.', '/app'], 'Copiando arquivos')

# Instala pacotes necessários
run_command(['pip', 'install', '--upgrade', 'pip'], 'Atualizando pip')
run_command(['pip', 'install', '-r', '/app/requirements.txt'], 'Instalando pacotes')

# Executa as migrações do banco de dados
run_command(['python', '/app/manage.py', 'migrate'], 'Executando migrações do banco de dados')

# Coleta os arquivos estáticos do Django
run_command(['python', '/app/manage.py', 'collectstatic'], 'Coletando arquivos estáticos do Django')

# Inicia o servidor web Gunicorn
run_command(['gunicorn', 'userApi.wsgi:application', '--bind', 'web:8000'], 'Iniciando servidor web')
