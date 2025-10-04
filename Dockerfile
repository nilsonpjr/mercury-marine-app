FROM python:3.9-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar as dependências do sistema para o Playwright no Debian Bullseye
# Esta lista é mais abrangente e compatível com o Playwright no Bullseye.
RUN apt-get update && apt-get install -y \
    build-essential \
    libnss3 \
    libxss1 \
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
    libasound2 \
    libfontconfig1 \
    libfreetype6 \
    libharfbuzz0b \
    libjpeg-dev \
    libpng-dev \
    libwebp-dev \
    libgconf-2-4 \
    libu2f-udev \
    libvulkan1 \
    libdbus-glib-1-2 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Instalar os navegadores do Playwright
RUN python3 -m playwright install --with-deps

COPY . .

# Definir a porta que a aplicação irá escutar
ENV PORT 8000
EXPOSE 8000

# Comando para rodar a aplicação com Gunicorn
CMD exec gunicorn --bind 0.0.0.0:$PORT app_playwright:app
