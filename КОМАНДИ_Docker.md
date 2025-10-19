# Швидкий довідник команд Docker

## Основні команди Docker

### Робота з образами
```bash
# Завантажити образ
docker pull <image_name>:<tag>

# Переглянути всі образи
docker images

# Видалити образ
docker rmi <image_id>
```

### Робота з контейнерами
```bash
# Запустити контейнер
docker run -d --name <container_name> <image_name>

# Переглянути працюючі контейнери
docker ps

# Переглянути всі контейнери
docker ps -a

# Зупинити контейнер
docker stop <container_name>

# Видалити контейнер
docker rm <container_name>

# Підключитися до контейнера
docker exec -it <container_name> <command>
```

### Збілд образу
```bash
# Збілдити образ з Dockerfile
docker build -t <image_name> .

# Збілдити з кешуванням
docker build --no-cache -t <image_name> .
```

## Docker Compose команди

### Основні операції
```bash
# Запустити всі сервіси
docker-compose up -d

# Запустити з перебілдом
docker-compose up -d --build

# Зупинити всі сервіси
docker-compose down

# Переглянути статус
docker-compose ps

# Переглянути логи
docker-compose logs

# Переглянути логи конкретного сервісу
docker-compose logs <service_name>
```

### Управління сервісами
```bash
# Запустити конкретний сервіс
docker-compose up -d <service_name>

# Зупинити конкретний сервіс
docker-compose stop <service_name>

# Перезапустити сервіс
docker-compose restart <service_name>
```

## Корисні команди для нашого проекту

### Запуск проекту
```bash
# Повний запуск
docker-compose up -d --build

# Перевірка статусу
docker-compose ps

# Перегляд логів
docker-compose logs -f
```

### Тестування
```bash
# Тест API
curl http://localhost:5000/api/stats

# Тест Redis
docker exec -it redis-container redis-cli ping

# Перегляд Redis даних
docker exec -it redis-container redis-cli
```

### Очищення
```bash
# Зупинити та видалити контейнери
docker-compose down

# Видалити також volumes
docker-compose down -v

# Видалити всі невикористовувані образи
docker system prune -a
```

## URL для доступу

- **Веб-додаток гри**: http://localhost:5000
- **Redis Commander**: http://localhost:8081
- **Redis API**: localhost:6379

## Структура файлів проекту

```
DevOps_pw3/
├── main.py                 # Оригінальна гра
├── Catcher.py             # Клас ловця
├── Egg.py                 # Клас яйця
├── Score.py               # Клас рахунку
├── RedisManager.py        # Менеджер Redis
├── web_server.py          # Flask веб-сервер
├── requirements.txt       # Python залежності
├── Dockerfile            # Docker образ
├── .dockerignore         # Ігнорування файлів
├── docker-compose.yml    # Docker Compose конфігурація
├── ЗВІТ_DevOps_Docker.md # Детальний звіт
└── КОМАНДИ_Docker.md     # Цей файл
```
