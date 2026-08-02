# Imagem base oficial do Python (slim para ser mais leve)
FROM python:3.12-slim

# Não criar .pyc e desativar buffering de stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho dentro do container
WORKDIR /app

# Instalar dependências de sistema (úteis para compilar libs Python)
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia só o requirements primeiro, para aproveitar cache de build
COPY requirements.txt /app/

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto
COPY . /app/

# Configura o módulo de settings do Django
ENV DJANGO_SETTINGS_MODULE=estudo1.settings

# Em desenvolvimento, manter DEBUG=True no settings.py é ok.
# Em produção, você pode sobrescrever via variável de ambiente:
# ENV DEBUG=False

# Expor a porta padrão do servidor Django
EXPOSE 8000

# Comando padrão:
# - aplica migrações
# - roda o servidor de desenvolvimento escutando em todas as interfaces
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]