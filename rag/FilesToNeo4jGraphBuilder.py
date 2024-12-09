from langchain_core.runnables import  RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser
from langchain_neo4j import Neo4jGraph
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOllama
from langchain_experimental.graph_transformers import LLMGraphTransformer
from neo4j import GraphDatabase
from yfiles_jupyter_graphs import GraphWidget
from langchain_community.vectorstores import Neo4jVector
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.neo4j_vector import remove_lucene_chars
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
import os
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from neo4j import  Driver
from werkzeug.utils import secure_filename
import time
import psycopg2
from neo4j import GraphDatabase
from PyPDF2 import PdfReader



class FilesToNeo4jGraphBuilder:
    def __init__(self):
        self.graph = None
        self.vector_index = None
        self.llm_transformer = None
        self.embeddings = None
        self._neo4j_graph_init()
        self._initialize_llm()
        self._initialize_embeddings()

    def _neo4j_graph_init(self):
        if self.wait_for_neo4j():
            time.sleep(20)
            graph = Neo4jGraph()
            print("Neo4j доступен, начинаем работу!")
            # Здесь вставьте код, который запускает вашу модель.
        else:
            print("Не удалось подключиться к Neo4j после нескольких попыток.")

    def _initialize_llm(self):
        """Инициализация модели LLM для преобразования графов."""
        self.llm_transformer = LLMGraphTransformer(
            llm=OllamaFunctions(model="llama3.1", temperature=0, format="json")
        )

    def _initialize_embeddings(self):
        """Инициализация модели эмбеддингов."""
        self.embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    def _allowed_file(self,filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {"PDF"}

    def wait_for_neo4j(self, retries=10, delay=5):
        for i in range(retries):
            try:
                # Пытаемся подключиться к базе данных
                print(f'uri = {os.environ["NEO4J_URI"]}, user_name = {os.environ["NEO4J_USERNAME"]}, password = {os.environ["NEO4J_PASSWORD"]}')
                driver = GraphDatabase.driver(os.environ["NEO4J_URI"], auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]))
                session = driver.session()
                session.close()
                return True
            except Exception as e:
                print(f"Ошибка подключения к Neo4j: {e}. Попытка {i + 1} из {retries}")
                time.sleep(delay)
        return False
    
    def load_and_process_files(self, files):
        """Загрузка, обработка и добавление нескольких файлов в граф Neo4j."""
        processed_files = []
        for file in files:
            if self._allowed_file(file.filename):
                filepath = secure_filename(file.filename)
                file.save(filepath)  # Сохраняем файл временно
                try:
                    txt_filepath = self._convert_to_txt(filepath)
                    processed_files.append(self._process_file(txt_filepath))
                finally:
                    os.remove(txt_filepath)  # Удаляем оригинальный файл
            else:
                print(f"Неверный тип файла: {file.filename}")
        return processed_files
    
    def _convert_to_txt(self, filepath):
        """Преобразование PDF в TXT."""
        if filepath.lower().endswith(".pdf"):
            txt_filepath = filepath.rsplit('.', 1)[0] + ".txt"
            try:
                with open(txt_filepath, "w", encoding="utf-8") as txt_file:
                    reader = PdfReader(filepath)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            txt_file.write(text + "\n")
                print(f"Файл {filepath} успешно преобразован в {txt_filepath}")
                return txt_filepath
            except Exception as e:
                raise ValueError(f"Ошибка при обработке файла {filepath}: {str(e)}")
            # finally:
            #     os.remove(filepath)
        return filepath

    def _process_file(self, filepath):
        """Обработка одного файла и добавление в граф."""
        loader = TextLoader(file_path=filepath)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=24)
        documents = text_splitter.split_documents(documents=docs)

        graph_documents = self.llm_transformer.convert_to_graph_documents(documents)
        self.graph.add_graph_documents(
            graph_documents,
            baseEntityLabel=True,
            include_source=True
        )
        print(f"Файл {filepath} обработан и добавлен в граф")
        return filepath
    
    def initialize_vector_index(self):
        """Инициализация векторного индекса для поиска."""
        self.vector_index = Neo4jVector.from_existing_graph(
            embeddings=self.embeddings,
            search_type="hybrid",
            node_label="Document",
            text_node_properties=["text"],
            embedding_node_property="embedding"
        )
    
    # def search(self, query):
    #     """Выполнение семантического поиска."""
    #     if not self.vector_index:
    #         raise RuntimeError("Векторный индекс не инициализирован.")
    #     retriever = self.vector_index.as_retriever()
    #     results = retriever.get_relevant_documents(query=query)
    #     return results

