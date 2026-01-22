from .db_connect import get_connection
import random

def generate_data():
    conn = get_connection()
    cur = conn.cursor()

    # ---- Départements
    depts = ["Informatique", "Mathématiques", "Physique", "Chimie", "Biologie"]
    for d in depts:
        cur.execute("INSERT INTO departements(nom) VALUES (%s) ON CONFLICT DO NOTHING", (d,))

    # ---- Formations et Modules
    niveaux = ['L1','L2','L3','M1','M2']
    formation_list = []
    for dept_id, dept_name in enumerate(depts, start=1):
        for n in niveaux:
            nom = f"{dept_name} {n}"
            nb_modules = random.randint(6, 9)
            cur.execute(
                "INSERT INTO formations(nom, dept_id, nb_modules, niveau) VALUES (%s,%s,%s,%s) RETURNING id",
                (nom, dept_id, nb_modules, n)
            )
            formation_id = cur.fetchone()[0]
            formation_list.append(formation_id)

            # Modules pour cette formation
            for i in range(1, nb_modules + 1):
                cur.execute(
                    "INSERT INTO modules(nom, credits, formation_id) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
                    (f"Module{i}_{nom}", random.randint(2,5), formation_id)
                )

    # ---- Étudiants (~13 000)
    etudiant_id = 1
    for f_id in formation_list:
        for i in range(1, 251):  # 250 étudiants par formation x 52 formations ≈ 13k
            cur.execute(
                "INSERT INTO etudiants(nom, prenom, formation_id, promo) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                (f"Nom{etudiant_id}", f"Prenom{etudiant_id}", f_id, random.randint(1,5))
            )
            etudiant_id += 1

    # ---- Professeurs (~400)
    for i in range(1, 401):
        dept_id = random.randint(1, len(depts))
        cur.execute(
            "INSERT INTO professeurs(nom, dept_id, specialite) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
            (f"Prof{i}", dept_id, f"Specialite{i}")
        )

    # ---- Salles (~20)
    for i in range(1, 21):
        cur.execute(
            "INSERT INTO salles(nom, capacite, type, batiment) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING",
            (f"Salle{i}", random.randint(30,100), "Mixte", f"Batiment{i}")
        )

    # ---- Utilisateurs admin/doyen/chefdep/prof/etudiant
    cur.execute(
        "INSERT INTO utilisateurs(username, password, role) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
        ("admin", "admin", "admin")
    )
    cur.execute(
        "INSERT INTO utilisateurs(username, password, role) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
        ("doyen", "doyen", "doyen")
    )
    cur.execute(
        "INSERT INTO utilisateurs(username, password, role) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
        ("chefdep", "chefdep", "chefdep")
    )
    cur.execute(
        "INSERT INTO utilisateurs(username, password, role) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
        ("prof1", "prof1", "professeur")
    )
    cur.execute(
        "INSERT INTO utilisateurs(username, password, role) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
        ("student1", "student1", "etudiant")
    )

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Données réalistes générées !")

if __name__ == "__main__":
    generate_data()
