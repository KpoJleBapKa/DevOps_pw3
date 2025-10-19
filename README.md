# Звіт з виконання практичної роботи №3
## Тема: "Освоєння Docker та Docker Compose"

**Студент:** [Ваше ім'я]  
**Група:** [Ваша група]  
**Дата:** 19.10.2025

---

## 1. Освоєння основних команд роботи з Docker

### 1.1 Pull та перегляд Docker images

**Команди:**
```bash
# Завантаження образів з Docker Hub
docker pull python:3.9-slim
docker pull redis:alpine

# Перегляд всіх завантажених образів
docker images
```

**Результат:**
```
REPOSITORY   TAG        IMAGE ID       CREATED       SIZE
python       3.9-slim   5af360dcfbbd   9 days ago    194MB
redis        alpine     59b6e6946534   2 weeks ago   100MB
```

### 1.2 Перегляд списку контейнерів

**Команди:**
```bash
# Перегляд працюючих контейнерів
docker ps

# Перегляд всіх контейнерів (включно з зупиненими)
docker ps -a
```

**Результат:** Спочатку контейнери відсутні, після запуску показує активні контейнери.

### 1.3 Видалення контейнерів та Docker images

**Команди:**
```bash
# Зупинка контейнера
docker stop redis-container

# Видалення контейнера
docker rm redis-container

# Видалення образу (якщо потрібно)
docker rmi <image_id>
```

### 1.4 Підключення до контейнеру через docker exec

**Команди:**
```bash
# Запуск контейнера Redis
docker run -d --name redis-container redis:alpine

# Підключення до контейнера та виконання команди
docker exec -it redis-container redis-cli ping
```

**Результат:** `PONG` - підтвердження успішного підключення до Redis.

---

## 2. Створення Dockerfile для проекту

### 2.1 Опис проекту

**Обраний проект:** Гра "Ловець" на Python з використанням tkinter
- `main.py` - основний файл гри
- `Catcher.py` - клас ловця
- `Egg.py` - клас яйця
- `Score.py` - клас рахунку

### 2.2 Створення Dockerfile

**Файл: `Dockerfile`**
```dockerfile
# Використовуємо офіційний Python образ
FROM python:3.9-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файли залежностей
COPY requirements.txt .

# Встановлюємо Python залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо файли проекту
COPY . .

# Встановлюємо залежності для GUI
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Відкриваємо порт для веб-сервера
EXPOSE 5000

# Команда для запуску веб-сервера
CMD ["python", "web_server.py"]
```

### 2.3 Створення .dockerignore

**Файл: `.dockerignore`**
```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
.git/
.gitignore
README.md
.env
node_modules/
```

### 2.4 Збілд Dockerfile

**Команда:**
```bash
docker build -t catcher-game .
```

**Результат:**
```
[+] Building 14.3s (9/9) FINISHED
 => [internal] load build definition from Dockerfile
 => [1/4] FROM docker.io/library/python:3.9-slim
 => [2/4] WORKDIR /app
 => [3/4] COPY . .
 => [4/4] RUN apt-get update && apt-get install -y python3-tk
 => exporting to image
 => naming to docker.io/library/catcher-game:latest
```

**Перевірка створеного образу:**
```bash
docker images
```
```
REPOSITORY     TAG        IMAGE ID       CREATED          SIZE
catcher-game   latest     e8b6eb4fab02   10 seconds ago   274MB
```

---

## 3. Додавання Redis сервісу та створення Docker Compose

### 3.1 Модифікація проекту для роботи з Redis

**Створені файли:**
- `RedisManager.py` - клас для роботи з Redis
- `web_server.py` - Flask веб-сервер замість GUI
- `requirements.txt` - залежності проекту

**Файл: `requirements.txt`**
```
redis==4.5.4
flask==2.3.3
```

### 3.2 Створення docker-compose.yml

**Файл: `docker-compose.yml`**
```yaml
version: '3.8'

services:
  # Веб-сервіс гри "Ловець"
  catcher-game:
    build: .
    container_name: catcher-game-container
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    ports:
      - "5000:5000"
    depends_on:
      - redis
    networks:
      - game-network

  # Redis сервіс для збереження результатів
  redis:
    image: redis:alpine
    container_name: redis-container
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - game-network
    command: redis-server --appendonly yes

  # Додатковий сервіс - веб-інтерфейс для перегляду статистики
  redis-commander:
    image: rediscommander/redis-commander:latest
    container_name: redis-commander
    environment:
      - REDIS_HOSTS=local:redis:6379
    ports:
      - "8081:8081"
    depends_on:
      - redis
    networks:
      - game-network

volumes:
  redis_data:

networks:
  game-network:
    driver: bridge
```

### 3.3 Запуск Docker Compose

**Команди:**
```bash
# Запуск всіх сервісів
docker-compose up -d --build

# Перегляд статусу сервісів
docker-compose ps
```

**Результат:**
```
NAME                     IMAGE                                   COMMAND                  SERVICE           CREATED          STATUS                    PORTS
catcher-game-container   devops_pw3-catcher-game                 "python web_server.py"   catcher-game      11 minutes ago   Up 11 minutes             0.0.0.0:5000->5000/tcp
redis-commander          rediscommander/redis-commander:latest   "/usr/bin/dumb-init …"   redis-commander   11 minutes ago   Up 11 minutes (healthy)   0.0.0.0:8081->8081/tcp
redis-container          redis:alpine                            "docker-entrypoint.s…"   redis             11 minutes ago   Up 11 minutes             0.0.0.0:6379->6379/tcp
```

---

## 4. Тестування та перевірка роботи

### 4.1 Перевірка API

**Команда:**
```bash
Invoke-WebRequest -Uri http://localhost:5000/api/stats -UseBasicParsing
```

**Результат:**
```json
{
  "recent_scores": [],
  "redis_connected": true,
  "total_games": 0
}
```

### 4.2 Доступні сервіси

1. **Веб-інтерфейс гри**: http://localhost:5000
   - Статистика ігор
   - Симуляція результатів
   - Перегляд підключення до Redis

2. **Redis Commander**: http://localhost:8081
   - Веб-інтерфейс для управління Redis
   - Перегляд даних в реальному часі

---

## 5. Висновки

### 5.1 Виконані завдання

✅ **Завдання 1**: Освоєно основні команди Docker:
- Pull та перегляд Docker images
- Перегляд списку контейнерів
- Видалення контейнерів/images
- Підключення до контейнеру через docker exec

✅ **Завдання 2**: Створено Dockerfile для проекту:
- Обрано проект гри "Ловець"
- Створено Dockerfile з оптимізацією
- Успішно збілдено Docker образ

✅ **Завдання 3**: Додано Redis сервіс та створено Docker Compose:
- Додано Redis для збереження результатів
- Створено docker-compose.yml з 3 сервісами
- Один сервіс з власного Dockerfile, два з Docker Hub

### 5.2 Створена архітектура

```
                    Docker Compose Network
    ┌─────────────────────────────────────────────────────────┐
    │                                                         │
    │  ┌─────────────────┐    ┌─────────────────┐            │
    │  │   Catcher Game  │    │      Redis      │            │
    │  │   (Flask App)   │◄──►│   (Database)    │            │
    │  │   Port: 5000    │    │   Port: 6379    │            │
    │  │                 │    │                 │            │
    │  │ - Веб-інтерфейс │    │ - Збереження    │            │
    │  │ - API endpoints │    │   результатів   │            │
    │  │ - Симуляція     │    │ - Статистика    │            │
    │  └─────────────────┘    └─────────────────┘            │
    │           │                       ▲                    │
    │           │                       │                    │
    │           ▼                       │                    │
    │  ┌─────────────────┐              │                    │
    │  │ Redis Commander │              │                    │
    │  │ (Web Interface) │──────────────┘                    │
    │  │   Port: 8081    │                                  │
    │  │                 │                                  │
    │  │ - Управління    │                                  │
    │  │   Redis         │                                  │
    │  │ - Перегляд даних│                                  │
    │  └─────────────────┘                                  │
    └─────────────────────────────────────────────────────────┘
                              │
                              ▼
                    Зовнішній доступ:
                    - http://localhost:5000 (Гра)
                    - http://localhost:8081 (Redis Commander)
```

### 5.3 Набуті навички

1. **Docker команди**: Освоєно базові операції з контейнерами та образами
2. **Dockerfile**: Навчився створювати оптимізовані Docker образи
3. **Docker Compose**: Створено мультисервісну архітектуру
4. **Мікросервіси**: Реалізовано взаємодію між сервісами
5. **Веб-розробка**: Адаптовано GUI додаток до веб-інтерфейсу

### 5.4 Практичне застосування

Створена система демонструє:
- Контейнеризацію Python додатків
- Використання зовнішніх сервісів (Redis)
- Веб-інтерфейси для управління
- Автоматизацію розгортання через Docker Compose

---

**Дата завершення:** 19.10.2025  
**Час виконання:** ~2 години  
**Статус:** ✅ Всі завдання виконано успішно
