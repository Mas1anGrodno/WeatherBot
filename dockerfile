# Используем официальный образ Python
#FROM python:alpine
FROM python:3.11-slim
# Устанавливаем рабочую директорию
WORKDIR /app

# Обновление pip python
RUN pip install --upgrade pip

# Копируем файлы requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Запускаем бота
CMD ["python", "weather_bot.py"]
