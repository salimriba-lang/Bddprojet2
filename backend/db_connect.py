import os
from urllib.parse import urlparse
import pg8000.native
import ssl

def get_connection():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        raise Exception("DATABASE_URL non défini. Vérifie tes variables d'environnement Railway.")

    result = urlparse(DATABASE_URL)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    # SSL requis pour Railway
    ssl_context = ssl.create_default_context()

    conn = pg8000.native.Connection(
        user=username,
        password=password,
        host=hostname,
        port=port,
        database=database,
        ssl_context=ssl_context
    )
    return conn
