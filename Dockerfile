FROM python:3.11.2

# Defina o diretório de trabalho como /app
WORKDIR /app

# Copie o script de inicialização para o contêiner
COPY .github/scripts/start.sh /start.sh
RUN chmod +x /start.sh

# Defina o script de inicialização como ponto de entrada
ENTRYPOINT ["/start.sh"]



