import React, { useState, useEffect, useRef } from 'react';
import '../App.css'; // импортируем файл стилей

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isChatStarted, setIsChatStarted] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const messagesEndRef = useRef(null);  // Для автоматической прокрутки вниз

  // Автоматическая прокрутка вниз после добавления нового сообщения
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();  // Прокручиваем вниз, когда добавляется новое сообщение
  }, [messages]);

  // Загружаем сохраненные данные из localStorage при первом рендере
  useEffect(() => {
    const savedMessages = JSON.parse(localStorage.getItem('messages'));
    const savedFiles = JSON.parse(localStorage.getItem('uploadedFiles'));
    const savedIsChatStarted = JSON.parse(localStorage.getItem('isChatStarted'));

    if (savedMessages) setMessages(savedMessages);
    if (savedFiles) setUploadedFiles(savedFiles);
    if (savedIsChatStarted) {
      setIsChatStarted(savedIsChatStarted);
    }
  }, []);

  // Измененная логика отправки сообщений
  const sendMessage = async (message) => {
    setMessages((prevMessages) => {
      const updatedMessages = [...prevMessages, { text: message, sender: "user" }];
      localStorage.setItem('messages', JSON.stringify(updatedMessages));  // Сохраняем в localStorage
      return updatedMessages;
    });
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        body: JSON.stringify({ message }), // Отправляем только сообщение на бэкэнд
        headers: {
          "Content-Type": "application/json"
        }
      });
      const data = await response.json();

      setMessages((prevMessages) => {
        const updatedMessages = [...prevMessages, { text: data.reply, sender: "bot" }];
        localStorage.setItem('messages', JSON.stringify(updatedMessages));  // Сохраняем в localStorage
        return updatedMessages;
      });
    } catch (error) {
      setMessages((prevMessages) => {
        const updatedMessages = [...prevMessages, { text: "Error: Unable to get response", sender: "bot" }];
        localStorage.setItem('messages', JSON.stringify(updatedMessages));  // Сохраняем в localStorage
        return updatedMessages;
      });
    }

    setLoading(false);
  };

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    const pdfFiles = selectedFiles.filter((file) => file.type === "application/pdf");

    if (pdfFiles.length > 0) {
      setUploadedFiles(pdfFiles);
      localStorage.setItem('uploadedFiles', JSON.stringify(pdfFiles));  // Сохраняем файлы в localStorage
    } else {
      alert("Please upload only PDF files!");
    }
  };

  const startNewChat = () => {
    setMessages([]);
    setUploadedFiles([]);
    setIsChatStarted(false);
    setInput("");

    // Очистить localStorage
    localStorage.removeItem('messages');
    localStorage.removeItem('uploadedFiles');
    localStorage.removeItem('isChatStarted');
  };

  // Новая логика старта чата и отправки файлов сразу
  const handleStartChat = async () => {
    setIsChatStarted(true);
    localStorage.setItem('isChatStarted', JSON.stringify(true));  // Сохраняем флаг в localStorage

    // Отправляем файлы на сервер сразу после старта чата
    if (uploadedFiles.length > 0) {
      const formData = new FormData();
      uploadedFiles.forEach((file) => {
        formData.append("file", file);
      });

      try {
        // Отправка файлов на сервер
        const response = await fetch("http://localhost:5000/upload-files", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error("Failed to upload files");
        }

        const data = await response.json();
        console.log("Files uploaded successfully:", data);
      } catch (error) {
        console.error("Error uploading files:", error);
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && input.trim()) {
      sendMessage(input);
    }
  };

  return (
    <div className={`chat-container ${isChatStarted ? 'started' : ''}`}>
      {!isChatStarted ? (
        <div>
          <h2>Upload PDF files to start the chat</h2>
          <input type="file" onChange={handleFileChange} accept="application/pdf" multiple />
          {uploadedFiles.length > 0 && (
            <div className="uploaded-files">
              <h3>Uploaded Files:</h3>
              <ul>
                {uploadedFiles.map((file, index) => (
                  <li key={index}>{file.name}</li>
                ))}
              </ul>
              <button onClick={handleStartChat}>Start Chat</button>
            </div>
          )}
        </div>
      ) : (
        <div className="chat-content">
          <div className="messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender}`}>
                <p>{msg.text}</p>
              </div>
            ))}
            <div ref={messagesEndRef} /> {/* Место для прокрутки */}
          </div>
          <div className="input-container">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}  // Обработчик нажатия Enter
              placeholder="Type your message..."
            />
            <button onClick={() => sendMessage(input)} disabled={loading || !input}>
              Send
            </button>
          </div>
          {loading && <p className="loading">Loading...</p>}
          <button onClick={startNewChat}>Start New Chat</button>
        </div>
      )}
    </div>
  );
}

export default Chat;
