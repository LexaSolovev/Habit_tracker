# Habit Tracker - Трекер привычек

## 🚀 Продакшен деплой
### 1. Подготовка сервера
```bash

# Установите Docker и Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo usermod -aG docker $USER
# Выйдите и заново войдите в систему
```
### 2. Клонирование и настройка
```bash

# Клонируйте репозиторий
git clone git@github.com:LexaSolovev/Habit_tracker.git /opt/habit-tracker
cd /opt/habit-tracker

# Скопируйте файл с примером переменных окружения и настройте его
cp .env_sample .env
nano .env  # Отредактируйте файл (SECRET_KEY, DEBUG=False, ALLOWED_HOSTS=ваш-домен)
```
### 3. Автоматический деплой

Используйте готовые скрипты для управления приложением:
bash

#### Сделайте скрипты исполняемыми
```bash 
chmod +x deploy/*.sh 
```

#### Первоначальная настройка сервера (только при первом развертывании)
```bash
./deploy/setup-server.sh
```

#### Основной скрипт деплоя
```bash
./deploy/deploy.sh
```

## Структура проекта:

```
├── .github/workflows/          # Конфигурация GitHub Actions CI/CD
│   └── ci-cd.yml
├── config/                     # Настройки Django проекта
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── habits/                     # Приложение "Привычки"
├── users/                      # Приложение "Пользователи"
├── deploy/                     # Скрипты для деплоя на сервер
├── nginx/                      # Конфигурация Nginx
│   └── nginx.conf
├── docker-compose.yml          # Конфигурация для разработки
├── docker-compose.prod.yml     # Конфигурация для production
├── Dockerfile                  # Образ для Django, Celery
├── .env_sample                 # Пример переменных окружения
├── requirements.txt            # Зависимости Python
├── manage.py
└── README.md
```
