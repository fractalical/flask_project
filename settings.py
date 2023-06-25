import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')
DATABASE_USER = os.getenv('DATABASE_USER', 'postgres')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'postgres')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'postgres')
