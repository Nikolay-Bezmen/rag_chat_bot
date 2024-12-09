import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'; // Подключаем стили
import App from './App'; // Подключаем компонент App

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root') // Рендерим в элемент с id="root"
);
