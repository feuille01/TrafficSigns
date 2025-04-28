from sqlalchemy import create_engine

# Данные подключения к MSSQL
servername = r'DESKTOP-J4V9VB5\SQLEXPRESS'  # Имя сервера с экземпляром
dbname = 'TrafficSignsGIBDD'

# Строка подключения к MSSQL с Windows Authentication
mssql_connection_string = f"mssql+pyodbc://@{servername}/{dbname}?trusted_connection=yes&driver=ODBC Driver 17 for SQL Server"

mssql_engine = create_engine(mssql_connection_string)

try:
    with mssql_engine.connect() as conn:
        print("Успешное подключение к MS SQL Server")
except Exception as e:
    print(f"Ошибка подключения к MS SQL Server: {e}")

# Данные подключения к PostgreSQL
pg_server = 'localhost'
pg_database = 'TrafficSignsCommercial'
pg_username = 'postgres'
pg_password = 'admin'

# Строка подключения к PostgreSQL
pg_connection_string = f"postgresql+psycopg2://{pg_username}:{pg_password}@{pg_server}/{pg_database}"

pg_engine = create_engine(pg_connection_string)

try:
    with pg_engine.connect() as conn:
        print("Успешное подключение к PostgreSQL")
except Exception as e:
    print(f"Ошибка подключения к PostgreSQL: {e}")
