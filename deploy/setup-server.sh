#!/bin/bash

# Скрипт первоначальной настройки сервера для Habit Tracker
# Выполняется один раз при настройке нового сервера

set -e

echo "=========================================="
echo "🛠️  Настройка сервера для Habit Tracker"
echo "=========================================="

# Обновление системы
echo "1. Обновление системы..."
sudo apt update
sudo apt upgrade -y

# Установка необходимых утилит
echo "2. Установка утилит..."
sudo apt install -y curl git nano htop

# Установка Docker
echo "3. Установка Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo rm get-docker.sh

# Установка Docker Compose
echo "4. Установка Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Настройка прав
echo "5. Настройка прав..."
sudo usermod -aG docker $USER

# Создание директории проекта
echo "6. Создание структуры проекта..."
sudo mkdir -p /opt/habit-tracker/{logs,backups,deploy,nginx}
sudo chown -R $USER:$USER /opt/habit-tracker

echo "=========================================="
echo "✅ Настройка сервера завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Выйдите и зайдите заново для применения прав Docker"
echo "2. Скопируйте файлы проекта в /opt/habit-tracker"
echo "3. Настройте .env файл"
echo "4. Запустите деплой: ./deploy.sh"
echo "=========================================="