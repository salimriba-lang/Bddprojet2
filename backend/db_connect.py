# backend/db_connect.py
import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

# Charger les variables d'environnement locales depuis .env (pour tests locaux)
load_dotenv()

def get_connection():
    """
    Retourne une connexion psycopg2 à PostgreSQL.
    Priorité :
    1. DATABASE_URL si elle est définie
    2. Sinon, utilise les variables séparées PGHOST, PGUSER, PGPASSWORD, PGDATABASE, PGPORT
    """

    # 1️⃣ Essayer DATABASE_URL (Railway ou .env)
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if DATABASE_URL:
        # Parse l'URL pour psycopg2
        result = urlparse(DATABASE_URL)
        username = result.username
        password = result.password
        database = result.path[1:]  # enlever le slash initial
        hostname = result.hostname
        port = result.port
    else:
        # 2️⃣ Sinon utiliser les variables PostgreSQL fournies par Railway
        hostname = os.getenv("PGHOST")
        port = os.getenv("PGPORT")
        username = os.getenv("PGUSER")
        password = os.getenv("PGPASSWORD")
        database = os.getenv("PGDATABASE")

        # Vérifie que toutes les infos sont présentes
        if not all([hostname, port, username, password, database]):
            raise Exception(
                "Informations DB manquantes. Vérifie DATABASE_URL ou les variables PGHOST/PGUSER/etc."
            )

    # 3️⃣ Connexion PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname=database,
            user=username,
            password=password,
            host=hostname,
            port=port,
            sslmode='require'  # requis pour Railway
        )
        return conn
    except Exception as e:
        raise Exception(f"Erreur connexion DB : {e}")
