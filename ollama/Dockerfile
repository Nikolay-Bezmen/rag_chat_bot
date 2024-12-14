FROM ubuntu:20.04

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y curl

# Устанавливаем Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Задаём команду по умолчанию
CMD ["ollama", "serve"]
