from backend.db_connect import get_connection
import random

def generate_data():
    conn = get_connection()
    cur = conn.cursor()

    depts = ["Informatique","Mathematiques","Physique","Chimie","Biologie"]
    for d in depts:
        cur.execute("INSERT IGNORE INTO departements(nom) VALUES (%s)", (d,))

    niveaux = ['L1','L2','L3','M1','M2']
    for dept_id in range(1, len(depts)+1):
        for n in niveaux:
            nom = f"{depts[dept_id-1]} {n}"
            cur.execute(
                "INSERT INTO formations(nom, dept_id, nb_modules, niveau) VALUES (%s,%s,%s,%s)",
                (nom, dept_id, random.randint(6,9), n)
            )

    cur.execute("SELECT id FROM formations")
    formations = cur.fetchall()

    for f in formations:
        for i in range(1, random.randint(6,9)):
            cur.execute(
                "INSERT INTO modules(nom, credits, formation_id) VALUES (%s,%s,%s)",
                (f"Module{i}", random.randint(2,5), f[0])
            )

    for f in formations:
        for i in range(1, 21):
            cur.execute(
                "INSERT INTO etudiants(nom, prenom, formation_id, promo) VALUES (%s,%s,%s,%s)",
                (f"Nom{i}", f"Prenom{i}", f[0], random.randint(1,5))
            )

    for i in range(1, 16):
        cur.execute(
            "INSERT INTO professeurs(nom, dept_id, specialite) VALUES (%s,%s,%s)",
            (f"Prof{i}", random.randint(1,5), "Specialite")
        )

    for i in range(1, 11):
        cur.execute(
            "INSERT INTO salles(nom, capacite, type, batiment) VALUES (%s,%s,%s,%s)",
            (f"Salle{i}", random.randint(10,20), "Mixte", f"Batiment{i}")
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Données générées (MySQL)")
