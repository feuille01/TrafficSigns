from flask import Flask, jsonify
from sqlalchemy import create_engine, text
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех маршрутов

# Подключение к PostgreSQL
# Данные подключения к PostgreSQL
pg_server = 'localhost'
pg_database = 'TrafficSignsCommercial'
pg_username = 'postgres'
pg_password = 'admin'

# Строка подключения к PostgreSQL
pg_connection_string = f"postgresql+psycopg2://{pg_username}:{pg_password}@{pg_server}/{pg_database}"
engine = create_engine(pg_connection_string)

@app.route('/api/signs')
def get_signs():
    try:
        query = text("SELECT * FROM merged_signs")
        with engine.connect() as conn:
            result = conn.execute(query)
            signs = [dict(row) for row in result.mappings()]
        return jsonify(signs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)