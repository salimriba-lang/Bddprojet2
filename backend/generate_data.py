from backend.db_connect import get_connection
import random

def generate_data():
    conn = get_connection()
    cur = conn.cursor()

    depts = ["Informatique","Mathematiques","Physique","Chimie","Biologie"]
    for d in depts:
        cur.execute("INSERT INTO departements(nom) VALUES (%s) ON CONFLICT DO NOTHING", (d,))

    niveaux = ['L1','L2','L3','M1','M2']
    for dept_id in range(1,len(depts)+1):
        for n in niveaux:
            nom = f"{depts[dept_id-1]} {n}"
            nb_modules = random.randint(6,9)
            cur.execute("INSERT INTO formations(nom, dept_id, nb_modules, niveau) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                        (nom, dept_id, nb_modules, n))

    cur.execute("SELECT id FROM formations")
    formations = cur.fetchall()
    for f in formations:
        for i in range(1, random.randint(6,9)+1):
            cur.execute("INSERT INTO modules(nom, credits, formation_id) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
                        (f"Module{i}", random.randint(2,5), f[0]))

    for f in formations:
        for i in range(1,21):
            cur.execute("INSERT INTO etudiants(nom, prenom, formation_id, promo) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                        (f"Nom{i}", f"Prenom{i}", f[0], random.randint(1,5)))

    for i in range(1,16):
        dept_id = random.randint(1,len(depts))
        cur.execute("INSERT INTO professeurs(nom, dept_id, specialite) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
                    (f"Prof{i}", dept_id, "Specialite"))

    for i in range(1,11):
        cur.execute("INSERT INTO salles(nom, capacite, type, batiment) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                    (f"Salle{i}", random.randint(10,20), "Mixte", f"Batiment{i}"))

    conn.commit()
    cur.close()
    conn.close()
    print("Données de test générées avec succès !")
