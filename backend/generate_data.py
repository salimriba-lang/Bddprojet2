from .db_connect import get_connection
import random

def generate_data():
    conn = get_connection()
    cur = conn.cursor()

    # ---- Départements
    depts = ["Informatique", "Mathematiques", "Physique", "Chimie", "Biologie"]
    for d in depts:
        cur.execute("INSERT INTO departements(nom) VALUES (%s) ON CONFLICT DO NOTHING", (d,))

    # ---- Formations et Modules
    niveaux = ['L1','L2','L3','M1','M2']
    for dept_id, dept_name in enumerate(depts, start=1):
        for n in niveaux:
            nom = f"{dept_name} {n}"
            nb_modules = random.randint(6,9)
            cur.execute("INSERT INTO formations(nom, dept_id, nb_modules, niveau) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                        (nom, dept_id, nb_modules, n))

    # Récupérer les formations
    cur.execute("SELECT id FROM formations")
    formations = [f[0] for f in cur.fetchall()]

    # Modules
    module_list = []
    for f in formations:
        for i in range(1, random.randint(6,9)+1):
            cur.execute("INSERT INTO modules(nom, credits, formation_id) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
                        (f"Module{i}_F{f}", random.randint(2,5), f))
            module_list.append(cur.lastrowid if hasattr(cur, 'lastrowid') else i)

    # ---- Étudiants (environ 13k)
    etudiant_id = 1
    for f in formations:
        for i in range(1, 251):  # 5 formations * 26 classes = ~13k
            cur.execute("INSERT INTO etudiants(nom, prenom, formation_id, promo) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                        (f"Nom{etudiant_id}", f"Prenom{etudiant_id}", f, random.randint(1,5)))
            etudiant_id += 1

    # ---- Professeurs (environ 400)
    for i in range(1, 401):
        dept_id = random.randint(1, len(depts))
        cur.execute("INSERT INTO professeurs(nom, dept_id, specialite) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
                    (f"Prof{i}", dept_id, f"Specialite{i}"))

    # ---- Salles
    for i in range(1, 21):
        cur.execute("INSERT INTO salles(nom, capacite, type, batiment) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                    (f"Salle{i}", random.randint(20,100), "Mixte", f"Batiment{i}"))

    conn.commit()
    cur.close()
    conn.close()
    print("Données réalistes générées !")

if __name__ == "__main__":
    generate_data()
