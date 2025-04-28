import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from geopy.distance import geodesic

# Данные подключения к MS SQL Server
servername = r'DESKTOP-J4V9VB5\SQLEXPRESS'
dbname = 'TrafficSignsGIBDD'

mssql_connection_string = f"mssql+pyodbc://@{servername}/{dbname}?trusted_connection=yes&driver=ODBC Driver 17 for SQL Server"

mssql_engine = create_engine(mssql_connection_string)

# Получение данных из таблицы Yekaterinburg_Locations_v2 в MS SQL Server
def get_data_from_mssql(table_name):
    query = f"SELECT * FROM {table_name}"
    try:
        with mssql_engine.connect() as conn:
            return pd.read_sql(query, conn)
    except Exception as e:
        print(f"Ошибка при извлечении данных из MS SQL Server: {e}")

gibdd_data = get_data_from_mssql('Yekaterinburg_Locations_v2')
print(gibdd_data.head())

# Данные подключения к PostgreSQL
pg_server = 'localhost'
pg_database = 'TrafficSignsCommercial'
pg_username = 'postgres'
pg_password = 'admin'

# Строка подключения к PostgreSQL
pg_connection_string = f"postgresql+psycopg2://{pg_username}:{pg_password}@{pg_server}/{pg_database}"

pg_engine = create_engine(pg_connection_string)

# Получение данных из таблицы с коммерческими знаками в PostgreSQL
def get_data_from_pg(table_name):
    query = f"SELECT * FROM {table_name}"
    try:
        with pg_engine.connect() as conn:
            return pd.read_sql(query, conn)
    except Exception as e:
        print(f"Ошибка при извлечении данных из PostgreSQL: {e}")

# Получение данных из таблицы с коммерческими знаками
commercial_data = get_data_from_pg('yekaterinburg_locations ')  # Имя таблицы
print(commercial_data.head())

# Обработка гибдд данных
def normalize_gibdd_coordinates(df):
    # Преобразуем координаты в градусы с плавающей точкой, деля на 100000
    df['latitude'] = df['latitude'].apply(lambda x: round(x / 1000000.0, 6))
    df['longitude'] = df['longitude'].apply(lambda x: round(x / 1000000.0, 6))
    return df

gibdd_data = normalize_gibdd_coordinates(gibdd_data)

# Обработка коммерции
def split_commercial_coordinates(df):
    coords = df['geo'].str.split(',', expand=True)
    df['latitude'] = coords[0].astype(float)
    df['longitude'] = coords[1].astype(float)
    return df

commercial_data = split_commercial_coordinates(commercial_data)

def normalize_commercial_coordinates(df):
    df['latitude'] = df['latitude'].round(6)
    df['longitude'] = df['longitude'].round(6)
    return df

commercial_data = normalize_commercial_coordinates(commercial_data)

# Нормализация названий знаков
def normalize_name(name):
    if pd.isnull(name):
        return ''
    return name.strip().replace(',', '').replace('.', '')

gibdd_data['name'] = gibdd_data['name'].apply(normalize_name)
commercial_data['name'] = commercial_data['name'].apply(normalize_name)

# Приводим таблицы к одному виду
gibdd_processed = pd.DataFrame({
    'name': gibdd_data['name'],
    'latitude': gibdd_data['latitude'],
    'longitude': gibdd_data['longitude'],
    'description': gibdd_data['description'],
    'source': 'gibdd',
    'gibdd_id': gibdd_data['id'],
    'commercial_id': None
})

commercial_processed = pd.DataFrame({
    'name': commercial_data['name'],
    'latitude': commercial_data['latitude'],
    'longitude': commercial_data['longitude'],
    'description': commercial_data['description'],
    'source': 'commercial',
    'gibdd_id': None,
    'commercial_id': commercial_data['internal_id']
})

merged = pd.concat([gibdd_processed, commercial_processed], ignore_index=True)

def merge_descriptions(desc1, desc2):
    # Фильтруем None и пустые строки
    descriptions = [d for d in [desc1, desc2] if d is not None and d.strip() != ""]
    # Объединяем через пробел
    return " ".join(descriptions)

# Обнаружение дублей
def merge_duplicates(df):
    to_remove = []
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            point1 = (df.loc[i, 'latitude'], df.loc[i, 'longitude'])
            point2 = (df.loc[j, 'latitude'], df.loc[j, 'longitude'])
            if geodesic(point1, point2).meters < 5:
                # объединяем описание
                combined_description = merge_descriptions(df.loc[i, 'description'], df.loc[j, 'description'])
                df.loc[i, 'description'] = combined_description
                df.loc[i, 'source'] = 'merged'
                if pd.isnull(df.loc[i, 'gibdd_id']):
                    df.loc[i, 'gibdd_id'] = df.loc[j, 'gibdd_id']
                if pd.isnull(df.loc[i, 'commercial_id']):
                    df.loc[i, 'commercial_id'] = df.loc[j, 'commercial_id']
                to_remove.append(j)
    df = df.drop(to_remove).reset_index(drop=True)
    return df
                # combined_description = (str(df.loc[i, 'description']) + ' ' + str(df.loc[j, 'description'])).strip()
    #             df.loc[i, 'description'] = combined_description
    #             df.loc[i, 'source'] = 'merged'
    #             if pd.isnull(df.loc[i, 'gibdd_id']):
    #                 df.loc[i, 'gibdd_id'] = df.loc[j, 'gibdd_id']
    #             if pd.isnull(df.loc[i, 'commercial_id']):
    #                 df.loc[i, 'commercial_id'] = df.loc[j, 'commercial_id']
    #             to_remove.append(j)
    # df = df.drop(to_remove).reset_index(drop=True)
    # return df

merged_final = merge_duplicates(merged)

# Загрузка в базу
try:
    with pg_engine.connect() as conn:
        merged_final.to_sql('merged_signs', conn, if_exists='append', index=False)
        print("Данные успешно загружены в merged_signs")
except Exception as e:
    print(f"Ошибка записи в merged_signs: {e}")
