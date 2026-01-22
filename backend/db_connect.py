import os
import pg8000.native
from urllib.parse import urlparse

def get_connection():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        raise Exception(
            "DATABASE_URL non défini. Vérifie tes variables d'environnement Railway."
        )

    # Parse l'URL
    result = urlparse(DATABASE_URL)
    user = result.username
    password = result.password
    host = result.hostname
    port = result.port
    database = result.path[1:]  # enlever le /

    # Connexion pg8000 avec SSL sans vérification
    conn = pg8000.native.Connection(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
        ssl=True,
        ssl_verify=False  # <- ignore le certificat self-signed
    )

    return conn
