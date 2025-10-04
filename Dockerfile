FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar as dependências do sistema para o Playwright
# Uma lista mais minimalista e comum para Playwright em ambientes Debian/Ubuntu
RUN apt-get update && apt-get install -y \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libdrm-dev \
    libgbm-dev \
    libglib2.0-0 \
    libgtk-3-0 \
    libxkbcommon-x11-0 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libxtst6 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Instalar os navegadores do Playwright
RUN python3 -m playwright install --with-deps

COPY . .

# Definir a porta que a aplicação irá escutar
ENV PORT 8000
EXPOSE 8000

# Comando para rodar a aplicação com Gunicorn
CMD exec gunicorn --bind 0.0.0.0:$PORT app_playwright:app

