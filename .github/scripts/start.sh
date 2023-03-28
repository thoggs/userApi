#!/bin/bash

# Cria o ambiente virtual na pasta .venv
python -m venv /app/.venv

# Ativa o ambiente virtual
source /app/.venv/bin/activate

# Define o caminho do sistema para o ambiente virtual
export PATH="/app/.venv/bin:$PATH"

# Cria a pasta static se ainda não existir
if [ ! -d "/app/static" ]; then
    mkdir -p /app/static
fi

# Copia os arquivos do projeto para o diretório /app
cp -r . /app

# Instala pacotes necessários
pip install --upgrade pip && pip install -r /app/requirements.txt

# Executa as migrações do banco de dados
python manage.py migrate

# Coleta os arquivos estáticos do Django
python manage.py collectstatic

# Inicia o servidor web Gunicorn
exec gunicorn userApi.wsgi:application --bind web:8000
