from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import requests
from PyPDF2 import PdfReader
import json
# import json
import os
# from FilesToNeo4jGraphBuilder import FilesToNeo4jGraphBuilder

from TextSimilarity import TextSimilarity
global text_similarity 
app = Flask(__name__)

# Настройка CORS
CORS(app, origins=["http://localhost:3000"])  # Разрешить фронтенд на 3000 порту


@app.route('/upload-files', methods=['POST'])
def upload_files():
    files = request.files.getlist('file')
    processed_files = []
    txt_file_pathes = []
    # Processing uploaded files
    for file in files:
        if not file.filename.endswith('.pdf'):
            return jsonify({"error": f"Файл {file.filename} не является PDF"}), 400
        try:
            # Save the uploaded file temporarily
            temp_path = os.path.join('/tmp', file.filename)
            file.save(temp_path)

            # Extract text from the PDF using PyPDF2
            pdf_reader = PdfReader(temp_path)
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()

            # Save the extracted text to a .txt file
            txt_filename = file.filename.rsplit('.', 1)[0] + '.txt'
            txt_file_path = os.path.join('/tmp', txt_filename)
            txt_file_pathes.append(txt_file_path)
            
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(pdf_text)

            # Add the text file info to the processed list
            processed_files.append({
                "original_filename": file.filename,
                "text_filename": txt_filename
            })

            # Clean up the temporary PDF file
            os.remove(temp_path)

        except Exception as e:
            return jsonify({"error": f"Ошибка при обработке файла {file.filename}: {str(e)}"}), 500
        
    global text_similarity
    text_similarity = TextSimilarity(txt_file_pathes)

    return jsonify({
        "message": "Файлы загружены и обработаны успешно",
        "processed_files": processed_files
    }), 200


# Эндпоинт для обработки сообщений
@app.route('/chat', methods=['POST'])
def chat():
    OLLAMA_API_URL = "http://172.17.0.1:1145/api/generate"
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Некорректный запрос, отсутствует поле 'message'"}), 400

    user_message = data['message']
    similar_chunks = text_similarity.find_most_similar_chunks("Giovanni and Maria's eldest son, inherited", top_n=5)
    similarity_data_answers = ""
    print("Most Similar Chunks:")
    for chunk, _ in similar_chunks:
        similarity_data_answers += f"{chunk}\n"

    query = f"Answer my question {user_message}. To do this, use the following data {similarity_data_answers}"
    req_data = {
        "model": "tinyllama",
        "prompt": query,
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
    
    

# Запуск приложения

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)




