import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

// Настройка иконок для разных источников
const iconGibdd = new L.Icon({
  iconUrl: '/icons/marker_blue.png',
  //shadowUrl: 'marker_blue.png',
  iconSize: [25, 25],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  //shadowSize: [41, 41]
});

const iconCommercial = new L.Icon({
  iconUrl: '/icons/marker_orange.png', // Путь к оранжевой иконке
  iconSize: [25, 25],                  // Размер иконки
  iconAnchor: [12, 41],                // Точка привязки иконки
  popupAnchor: [1, -34]                // Точка привязки всплывающего окна
});

function MapComponent({ signs }) {
  const center = [56.8345, 60.5933]; // Екатеринбург

  return (
    <MapContainer center={center} zoom={13} style={{ height: '100vh' }}>
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {signs.map(sign => (
        <Marker
          key={sign.id}
          position={[sign.latitude, sign.longitude]}
          icon={sign.source === 'gibdd' ? iconGibdd : iconCommercial}
        >
          <Popup>
            <div>
              <h3>{sign.name}</h3>
              <p><strong>Источник:</strong> {sign.source}</p>
              <p><strong>Описание:</strong> {sign.description || 'Нет описания'}</p>
              <p><strong>Координаты:</strong> {sign.latitude + ', ' + sign.longitude}</p>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default MapComponent;