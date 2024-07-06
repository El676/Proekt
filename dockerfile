# Используем официальный образ Nginx
FROM nginx:alpine

# Копируем статические файлы в директорию Nginx
COPY static /usr/share/nginx/html/static
COPY templates /usr/share/nginx/html/templates

# Копируем конфигурационный файл Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf