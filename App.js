import './App.css';
import MapComponent from './MapComponent';
import { useEffect, useState } from 'react';

function App() {
  const [signs, setSigns] = useState([]);

  useEffect(() => {
    // Загрузка данных через локальный сервер
    fetch('http://localhost:5000/api/signs')
      .then(response => response.json())
      .then(data => setSigns(data))
      .catch(error => console.error('Ошибка загрузки данных:', error));
  }, []);

  return (
    <div className="App">
      <h1>Карта дорожных знаков</h1>
      <MapComponent signs={signs} />
    </div>
  );
}

export default App;