# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем переменные среды для оптимальной работы Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /rag

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей в контейнер
COPY requirements.txt /rag/

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем содержимое текущей директории в контейнер
COPY . /rag

# Создаем директорию для загрузок
RUN mkdir -p /rag/uploads

# Указываем порт, на котором работает приложение
EXPOSE 5000

# Указываем команду для запуска приложения
CMD ["python", "rag_app.py"]
