FROM python:3.11.2

# Defina o diretório de trabalho como /app
WORKDIR /app

# Cria o ambiente virtual na pasta .venv
RUN python -m venv /app/.venv

# Ativa o ambiente virtual
RUN . /app/.venv/bin/activate

# Define o caminho do sistema para o ambiente virtual
RUN export PATH="/app/.venv/bin:$PATH"

# Copia os arquivos do projeto para o diretório /app
COPY . /app

# Instala pacotes necessários
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copie o script de inicialização para o contêiner
COPY .github/scripts/start.sh /start.sh
RUN chmod +x /start.sh

# Defina o script de inicialização como ponto de entrada
ENTRYPOINT ["/start.sh"]
