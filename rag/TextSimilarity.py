import nltk
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
nltk.download('punkt_tab')


# Загружаем модель для получения embedding
class TextSimilarity:
    def __init__(self, file_pathes, chunk_size=200):
        self.chunk_size = chunk_size
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunks = []
        self.embeddings = []
        self._load_and_process_text(file_pathes)
    
    # Функция для загрузки и обработки текста
    def _load_and_process_text(self, file_pathes: list):
        text_from_files = ""

        for file_path in file_pathes:
            with open(str(file_path), 'r', encoding='utf-8') as file:
                text_from_files += file.read()
        
        # Разбиение текста на chunks
        self.chunks = self.split_text_into_chunks(text_from_files)
        # Получение embeddings для всех chunks
        self.embeddings = self.get_embeddings(self.chunks)
    
    # Разбиение текста на chunks
    def split_text_into_chunks(self, text):
        sentences = nltk.sent_tokenize(text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk.split()) + len(sentence.split()) <= self.chunk_size:
                current_chunk += " " + sentence
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks

    # Получение embeddings для списка текстов (chunks)
    def get_embeddings(self, chunks):
        embeddings = self.model.encode(chunks)
        return embeddings

    # Поиск наиболее похожих chunks
    def find_most_similar_chunks(self, query_text, top_n=10):
        # Получаем embedding для запроса
        query_embedding = self.model.encode([query_text])
        
        # Вычисляем косинусное сходство между запросом и всеми chunks
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Получаем индексы наиболее схожих chunks
        similar_indices = similarities.argsort()[-top_n:][::-1]
        
        return [(self.chunks[i], similarities[i]) for i in similar_indices]

