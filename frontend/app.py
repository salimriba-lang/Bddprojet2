import streamlit as st
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.db_connect import get_connection
import pandas as pd

if 'login' not in st.session_state:
    st.session_state['login'] = False
    st.session_state['role'] = ''

def login():
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT role FROM utilisateurs WHERE username=%s AND password=%s", (username, password))
            result = cur.fetchone()
            if result:
                st.session_state['login'] = True
                st.session_state['role'] = result[0]
                st.success(f"Connecté comme {st.session_state['role']}")
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect")
        except Exception as e:
            st.error(f"Erreur connexion DB : {e}")
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()

if not st.session_state['login']:
    st.title("Connexion à la plateforme")
    login()
else:
    st.title(f"Dashboard {st.session_state['role']}")
    role = st.session_state['role']
    conn = get_connection()
    cur = conn.cursor()
    if role == 'doyen':
        st.subheader("Statistiques globales")
        cur.execute("SELECT COUNT(*) FROM salles")
        st.write("Nombre de salles :", cur.fetchone()[0])
        cur.execute("SELECT COUNT(*) FROM examens")
        st.write("Nombre d'examens :", cur.fetchone()[0])
    elif role == 'admin':
        st.subheader("Génération EDT")
        if st.button("Générer EDT"):
            from backend.generate_edt import generate_exam_schedule
            generate_exam_schedule()
    elif role == 'chefdep':
        st.subheader("Statistiques par département")
        cur.execute("SELECT COUNT(*) FROM formations")
        st.write("Nombre de formations :", cur.fetchone()[0])
    elif role == 'professeur':
        st.subheader("Mes examens")
        cur.execute("SELECT * FROM examens LIMIT 5")
        st.write(pd.DataFrame(cur.fetchall()))
    elif role == 'etudiant':
        st.subheader("Mon planning")
        cur.execute("SELECT * FROM examens LIMIT 5")
        st.write(pd.DataFrame(cur.fetchall()))
    cur.close()
    conn.close()
