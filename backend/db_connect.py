import os
import pg8000.native
from urllib.parse import urlparse

def get_connection():
    # Railway fournit DATABASE_URL de la forme postgres://user:pass@host:port/dbname
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        raise Exception("DATABASE_URL non défini. Vérifie tes variables d'environnement Railway.")
    
    result = urlparse(DATABASE_URL)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    conn = pg8000.native.Connection(
        user=username,
        password=password,
        database=database,
        host=hostname,
        port=port,
        ssl=True  # requis pour Railway
    )
    return conn
