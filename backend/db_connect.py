import os
import pg8000
from urllib.parse import urlparse

def get_connection():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        raise Exception(
            "DATABASE_URL non défini. Vérifie tes variables d'environnement Railway."
        )

    result = urlparse(DATABASE_URL)
    user = result.username
    password = result.password
    host = result.hostname
    port = result.port
    database = result.path[1:]

    # Utiliser pg8000.connect() (DBAPI) avec SSL
    conn = pg8000.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
        ssl_context=False  # <-- ignore les certificats auto-signés
    )

    return conn
