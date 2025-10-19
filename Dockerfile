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

# Встановлюємо залежності (tkinter вже включений в Python)
# Для GUI додатків на Linux потрібні додаткові пакети
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо змінну середовища для відображення GUI
ENV DISPLAY=:0

# Відкриваємо порт для веб-сервера
EXPOSE 5000

# Команда для запуску веб-сервера
CMD ["python", "web_server.py"]
