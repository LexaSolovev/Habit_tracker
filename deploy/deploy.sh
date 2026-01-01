#!/bin/bash

set -e

echo "=== Начало деплоя ==="

# Переход в директорию проекта
cd /opt/habit-tracker

# Создание .env файла из переменных окружения
echo "Создание .env файла..."

cat > .env << EOF
# Django
SECRET_KEY=${SECRET_KEY}
DEBUG=False
ALLOWED_HOSTS=${ALLOWED_HOSTS}

# Database
DB_PASSWORD=${DB_PASSWORD}
REDIS_PASSWORD=${REDIS_PASSWORD}

# Telegram
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}

# Docker
DOCKER_IMAGE=${DOCKER_IMAGE}
EOF

echo ".env файл создан"

# Проверка обязательных переменных
if [ -z "$SECRET_KEY" ]; then
    echo "ОШИБКА: SECRET_KEY не установлен"
    exit 1
fi

if [ -z "$DB_PASSWORD" ]; then
    echo "ОШИБКА: DB_PASSWORD не установлен"
    exit 1
fi

if [ -z "$ALLOWED_HOSTS" ]; then
    echo "ОШИБКА: ALLOWED_HOSTS не установлен"
    exit 1
fi

# Остановка старых контейнеров
echo "Остановка старых контейнеров..."
docker-compose -f docker-compose.prod.yml down || true

# Запуск контейнеров
echo "Запуск контейнеров..."
docker-compose -f docker-compose.prod.yml up -d --build

# Миграции базы данных
echo "Применение миграций..."
docker-compose -f docker-compose.prod.yml exec -T django python manage.py migrate

# Сбор статических файлов
echo "Сбор статических файлов..."
docker-compose -f docker-compose.prod.yml exec -T django python manage.py collectstatic --noinput

echo "=== Деплой завершен успешно ==="