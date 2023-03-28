FROM python:3.11.2

# Defina o diretório de trabalho como /app
WORKDIR /app

# Cria um ambiente virtual na pasta .venv
RUN python -m venv .venv

# Ativa o ambiente virtual e define o caminho do sistema para o ambiente virtual
ENV PATH="/app/.venv/bin:$PATH"
RUN /bin/bash -c "source /app/.venv/bin/activate && pip install --upgrade pip"

# Instale as dependências
RUN pip install tqdm

# Copie o script de inicialização para o contêiner
COPY .github/scripts/start.py /start.py
RUN chmod +x /start.py

# Defina o script de inicialização como ponto de entrada
ENTRYPOINT ["python", "/start.py"]
