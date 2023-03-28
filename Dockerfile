FROM python:3.11.2

# Defina o diretório de trabalho como /app
WORKDIR /app

# Instale as dependências
RUN pip install tqdm

# Copie o script de inicialização para o contêiner
COPY .github/scripts/start.py /start.py
RUN chmod +x /start.py

# Defina o script de inicialização como ponto de entrada
ENTRYPOINT ["/start.py"]
