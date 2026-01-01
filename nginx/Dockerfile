FROM nginx:1.25-alpine

# Удаляем дефолтную конфигурацию
RUN rm /etc/nginx/conf.d/default.conf

# Копируем нашу конфигурацию
COPY nginx/nginx.conf /etc/nginx/conf.d/

# Создаем директорию для статических файлов
RUN mkdir -p /var/www/static