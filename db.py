import psycopg2
from psycopg2 import sql
from config import config

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(config.DB_URI)
        self.schema = config.DB_SCHEMA
    
    def save_photo(self, file_name, image_data, mime_type):
        """Сохраняет фото в базу данных с автоматической обработкой"""
        query = sql.SQL("""
            INSERT INTO {schema}.photos (file_name, image_data, mime_type)
            VALUES (%s, %s, %s)
            RETURNING photo_id, file_size, created_at
        """).format(schema=sql.Identifier(self.schema))
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, (file_name, image_data, mime_type))
                result = cursor.fetchone()
                self.conn.commit()
                return {
                    'photo_id': result[0],
                    'file_size': result[1],
                    'created_at': result[2]
                }
        except Exception as e:
            self.conn.rollback()
            raise e
    
    def get_photo(self, photo_id):
        """Получает фото и метаданные по ID"""
        query = sql.SQL("""
            SELECT image_data, mime_type, file_name
            FROM {schema}.photos
            WHERE photo_id = %s
        """).format(schema=sql.Identifier(self.schema))
        
        with self.conn.cursor() as cursor:
            cursor.execute(query, (photo_id,))
            result = cursor.fetchone()
            if not result:
                return None
            return {
                'image_data': result[0],
                'mime_type': result[1],
                'file_name': result[2]
            }
    
    def close(self):
        self.conn.close()

# Инициализируем подключение при старте
db = Database()