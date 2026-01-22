import streamlit as st
from backend.db_connect import get_connection
import pandas as pd
import plotly.express as px
from backend.generate_edt import generate_exam_schedule

st.set_page_config(page_title="Plateforme EDT", layout="wide")

# Session
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
    role = st.session_state['role']
    st.title(f"Dashboard {role}")
    conn = get_connection()
    cur = conn.cursor()

    if role == 'admin':
        st.subheader("Génération de l'emploi du temps")
        if st.button("Générer EDT"):
            generate_exam_schedule()
            st.success("EDT généré !")
        st.subheader("Prévisualiser l'emploi du temps")
        cur.execute("SELECT e.date_exam, m.nom AS module, s.nom AS salle FROM examens e JOIN modules m ON e.module_id = m.id JOIN salles s ON e.salle_id = s.id")
        df = pd.DataFrame(cur.fetchall(), columns=["Date","Module","Salle"])
        st.dataframe(df)

    elif role == 'chefdep':
        st.subheader("Validation EDT département")
        cur.execute("SELECT e.date_exam, m.nom AS module, s.nom AS salle FROM examens e JOIN modules m ON e.module_id = m.id JOIN salles s ON e.salle_id = s.id LIMIT 20")
        df = pd.DataFrame(cur.fetchall(), columns=["Date","Module","Salle"])
        st.dataframe(df)
        if st.button("Confirmer EDT département"):
            st.success("EDT confirmé, envoyé au doyen")

    elif role == 'doyen':
        st.subheader("Validation finale et statistiques")
        cur.execute("SELECT e.date_exam, m.nom AS module, s.nom AS salle FROM examens e JOIN modules m ON e.module_id = m.id JOIN salles s ON e.salle_id = s.id")
        df = pd.DataFrame(cur.fetchall(), columns=["Date","Module","Salle"])
        st.dataframe(df)
        fig = px.bar(df, x="Date", y="Module", title="Nombre d'examens par date")
        st.plotly_chart(fig)

    elif role == 'professeur':
        st.subheader("Mes examens")
        cur.execute("SELECT e.date_exam, m.nom AS module, s.nom AS salle FROM examens e JOIN modules m ON e.module_id = m.id JOIN salles s ON e.salle_id = s.id LIMIT 10")
        df = pd.DataFrame(cur.fetchall(), columns=["Date","Module","Salle"])
        st.dataframe(df)

    elif role == 'etudiant':
        st.subheader("Mon planning")
        cur.execute("SELECT e.date_exam, m.nom AS module, s.nom AS salle FROM examens e JOIN modules m ON e.module_id = m.id JOIN salles s ON e.salle_id = s.id LIMIT 10")
        df = pd.DataFrame(cur.fetchall(), columns=["Date","Module","Salle"])
        st.dataframe(df)

    cur.close()
    conn.close()
