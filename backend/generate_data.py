from .db_connect import get_connection
import random

def generate_data():
    conn = get_connection()
    cur = conn.cursor()

    # ----- Départements -----
    depts = ["Informatique", "Mathématiques", "Physique", "Chimie", "Biologie"]
    for d in depts:
        cur.execute(
            "INSERT INTO departements(nom) VALUES (%s) ON CONFLICT DO NOTHING", (d,)
        )

    # ----- Formations et Modules -----
    niveaux = ['L1','L2','L3','M1','M2']
    formation_ids = []
    for dept_id, dept_name in enumerate(depts, start=1):
        for n in niveaux:
            nom = f"{dept_name} {n}"
            nb_modules = random.randint(6,9)
            cur.execute(
                "INSERT INTO formations(nom, dept_id, nb_modules, niveau) VALUES (%s,%s,%s,%s) RETURNING id",
                (nom, dept_id, nb_modules, n)
            )
            formation_id = cur.fetchone()[0]
            formation_ids.append(formation_id)

            # Modules pour cette formation
            for i in range(1, nb_modules+1):
                cur.execute(
                    "INSERT INTO modules(nom, credits, formation_id) VALUES (%s,%s,%s)",
                    (f"Module{i}_{nom}", random.randint(2,5), formation_id)
                )

    # ----- Étudiants (13 000) -----
    etudiant_id = 1
    for f_id in formation_ids:
        for _ in range(250):  # ~13k étudiants
            cur.execute(
                "INSERT INTO etudiants(nom, prenom, formation_id, promo) VALUES (%s,%s,%s,%s)",
                (f"Nom{etudiant_id}", f"Prenom{etudiant_id}", f_id, random.randint(1,5))
            )
            etudiant_id += 1

    # ----- Professeurs (400) -----
    for i in range(1, 401):
        dept_id = random.randint(1, len(depts))
        cur.execute(
            "INSERT INTO professeurs(nom, dept_id, specialite) VALUES (%s,%s,%s)",
            (f"Prof{i}", dept_id, f"Specialite{i}")
        )

    # ----- Salles (20) -----
    for i in range(1, 21):
        cur.execute(
            "INSERT INTO salles(nom, capacite, type, batiment) VALUES (%s,%s,%s,%s)",
            (f"Salle{i}", random.randint(20,100), "Mixte", f"Batiment{i}")
        )

    # ----- Utilisateurs pour tests -----
    users = [
        ("admin","admin123","admin"),
        ("doyen","doyen123","doyen"),
        ("chefdep","chefdep123","chefdep"),
        ("prof1","prof123","professeur"),
        ("etudiant1","etudiant123","etudiant")
    ]
    for username, password, role in users:
        cur.execute(
            "INSERT INTO utilisateurs(username,password,role) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
            (username,password,role)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Données réalistes générées !")

if __name__ == "__main__":
    generate_data()