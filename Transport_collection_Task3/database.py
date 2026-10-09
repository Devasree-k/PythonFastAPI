import psycopg
from config import Config


async def get_connection():
    return await psycopg.AsyncConnection.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD
    )

    