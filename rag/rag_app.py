from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import requests
import json
# import json

app = Flask(__name__)

# Настройка CORS
CORS(app, origins=["http://localhost:3000"])  # Разрешить фронтенд на 3000 порту

  # URL Ollama (если локально)

# Эндпоинт для обработки сообщений
@app.route('/chat', methods=['POST'])
def chat():
    OLLAMA_API_URL = "http://172.17.0.1:1145/api/generate"
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Некорректный запрос, отсутствует поле 'message'"}), 400

    user_message = data['message']

    # # Отправка запроса к API Ollama

    req_data = {
        "model": "tinyllama",
        "prompt": user_message,
        "stream": False
    }

    headers = {"Content-Type": "application/json"} 

    response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(req_data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        act_response = data['response']

        return jsonify({"reply": act_response})
    else:
        return jsonify({"code of error ": response.status_code,"text of response :": response.text})


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
    OLLAMA_API_URL = "http://172.17.0.1:1145/api/generate"
    req_data = {
        "model": "tinyllama",
        "prompt": "Hello, how are you?",
        "stream": False
    }

    headers = {"Content-Type": "application/json"} 
    response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(req_data))




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

