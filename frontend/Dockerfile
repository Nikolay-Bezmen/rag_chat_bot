# Используем официальный образ Node.js
FROM node:16

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /frontend

# Копируем только package.json и package-lock.json, если они есть
COPY package*.json ./

# Выполняем npm install для установки зависимостей
RUN npm install --verbose

# Копируем все остальные файлы проекта в контейнер
COPY . .

# Открываем порт для разработки
EXPOSE 3000

# Запускаем приложение
CMD ["npm", "start"]
