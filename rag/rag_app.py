from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import requests
# import json

app = Flask(__name__)

# Настройка CORS
CORS(app, origins=["http://localhost:3000"])  # Разрешить фронтенд на 3000 порту
OLLAMA_API_URL = "http://localhost:11434"  # URL Ollama (если локально)

# Эндпоинт для обработки сообщений
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Некорректный запрос, отсутствует поле 'message'"}), 400

    user_message = data['message']

    # Отправка запроса к API Ollama

    req_data = {
        "model": "llama2",
        "prompt": "Hello, how are you?"
    }

    headers = {"Content-Type": "application/json"} 

    response = requests.post(
        f"{OLLAMA_API_URL}/api/generate",
        json=req_data,
        headers=headers
    )
    response.raise_for_status()  # Выбрасывает исключение при HTTP-ошибках
    api_response = response.json()
    print("API Response:", api_response)  # Выводим ответ для диагностики
    bot_reply = api_response.get("completion", "Модель не дала ответа.")
    # try:
    #     response = requests.post(
    #         f"{OLLAMA_API_URL}/api/generate",
    #         json=req_data,
    #         headers=headers
    #     )
    #     response.raise_for_status()  # Выбрасывает исключение при HTTP-ошибках
    #     api_response = response.json()
    #     print("API Response:", api_response)  # Выводим ответ для диагностики
    #     bot_reply = api_response.get("completion", "Модель не дала ответа.")
    # except requests.RequestException as e:
    #     # return jsonify({"reply": "bot_reply"})
    #     return jsonify({"error": f"Ошибка подключения к Ollama: {str(e)}"}), 500

    if len(bot_reply) < 1:
        bot_reply = "huy"
    return jsonify({"reply": user_message})

# Эндпоинт для загрузки файлов (заглушка)
@app.route('/upload-files', methods=['POST'])
def upload_files():
    if 'file' not in request.files:
        return jsonify({"error": "Нет файлов в запросе"}), 400

    files = request.files.getlist('file')
    uploaded_files = []
    processed_files = []

    # for file in files:
    #     filename = secure_filename(file.filename)
    #     file.save(f"./uploads/{filename}")
    #     uploaded_files.append(filename)
    #     # Обработка файла может быть добавлена позже

    return jsonify({"message": "Файлы загружены успешно", "uploaded_files": uploaded_files})

# Запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# import requests

# url = "http://localhost:11434/api/generate"
# headers = {"Content-Type": "application/json"}
# data = {
#     "model": "llama2",
#     "prompt": "Hello, how are you?",
#     "stream": False
# }

# try:
#     response = requests.post(url, json=data, headers=headers)
#     response.raise_for_status()  # Проверка на HTTP-ошибки
#     print(response.json())  # Выводим ответ сервера
# except requests.exceptions.RequestException as e:
#     print(f"Ошибка при выполнении запроса: {e}")

