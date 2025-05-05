FROM python:3.11-slim

# Instala pacotes de sistema necessários
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do projeto
COPY . .

# Expondo a porta
EXPOSE 8000

# Comando para iniciar o app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
