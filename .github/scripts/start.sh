#!/bin/bash

echo "Loading..."

# Cria o ambiente virtual na pasta .venv com barra de progresso
python -m venv /app/.venv | pv -lep -s 100 > /dev/null

# Ativa o ambiente virtual com barra de progresso
source /app/.venv/bin/activate | pv -lep -s 100 > /dev/null

# Define o caminho do sistema para o ambiente virtual com barra de progresso
export PATH="/app/.venv/bin:$PATH" | pv -lep -s 100 > /dev/null

# Cria a pasta static se ainda não existir com barra de progresso
if [ ! -d "/app/static" ]; then
    mkdir -p /app/static | pv -lep -s 100 > /dev/null
fi

# Copia os arquivos do projeto para o diretório /app com barra de progresso
echo "Copying project files..."
cp -r . /app | pv -lep -s "$(du -sb . | awk '{print $1}')" > /dev/null

# Instala pacotes necessários com barra de progresso
echo "Installing required packages..."
pip install --no-cache-dir --progress-bar=auto --upgrade pip && pip install --no-cache-dir --progress-bar=auto -r /app/requirements.txt

# Executa as migrações do banco de dados com barra de progresso
echo "Running database migrations..."
python manage.py migrate | pv -lep -s 100 > /dev/null

# Coleta os arquivos estáticos do Django com barra de progresso
echo "Collecting Django static files..."
python manage.py collectstatic | pv -lep -s 100 > /dev/null

# Inicia o servidor web Gunicorn
echo "Starting Gunicorn web server..."
exec gunicorn userApi.wsgi:application --bind web:8000
