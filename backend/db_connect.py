import psycopg2
import os
from urllib.parse import urlparse

def get_connection():
    # Railway fournit DATABASE_URL de la forme postgres://user:pass@host:port/dbname
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        raise Exception("DATABASE_URL non défini. Vérifie tes variables d'environnement Railway.")
    
    # Parse l'URL pour psycopg2
    result = urlparse(DATABASE_URL)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port

    conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=hostname,
        port=port,
        sslmode='require'  # requis pour Railway
    )
    return conn
