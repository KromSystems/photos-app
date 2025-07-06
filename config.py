import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'postgres')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_SCHEMA = os.getenv('DB_SCHEMA', 'media')
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret-key')
    MAX_CONTENT_LENGTH = eval(os.getenv('MAX_CONTENT_LENGTH', '10 * 1024 * 1024'))
    
    @property
    def DB_URI(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

config = Config()