from .db_connect import get_connection
from datetime import datetime, timedelta
import random

def generate_exam_schedule():
    conn = get_connection()
    cur = conn.cursor()

    # ----- Supprimer les anciens examens et surveillances -----
    cur.execute("DELETE FROM examens")
    cur.execute("DELETE FROM surveillances")
    conn.commit()

    # ----- Récupérer tous les modules, salles et professeurs -----
    cur.execute("SELECT id FROM modules")
    modules = [m[0] for m in cur.fetchall()]

    cur.execute("SELECT id, capacite FROM salles")
    salles = cur.fetchall()

    cur.execute("SELECT id FROM professeurs")
    profs = [p[0] for p in cur.fetchall()]

    start_date = datetime.now()

    for module_id in modules:
        # Choisir salle adaptée aléatoire
        salle_id, capacite = random.choice(salles)

        # Nombre d'étudiants aléatoire pour le module
        nb_students_for_module = random.randint(30, 200)
        if nb_students_for_module > capacite:
            possible_salles = [s for s in salles if s[1] >= nb_students_for_module]
            if possible_salles:
                salle_id, capacite = random.choice(possible_salles)
            else:
                salle_id, capacite = max(salles, key=lambda s: s[1])

        # Insérer examen
        cur.execute(
            "INSERT INTO examens(module_id, salle_id, date_exam) VALUES (%s,%s,%s) RETURNING id",
            (module_id, salle_id, start_date.date())
        )
        examen_id = cur.fetchone()[0]

        # Assigner 1 à 3 profs aléatoires
        for _ in range(random.randint(1,3)):
            professeur_id = random.choice(profs)
            cur.execute(
                "INSERT INTO surveillances(examen_id, professeur_id) VALUES (%s,%s)",
                (examen_id, professeur_id)
            )

        # Jour suivant
        start_date += timedelta(days=1)
        if start_date.weekday() == 4:  # Skip vendredi
            start_date += timedelta(days=1)

    conn.commit()
    cur.close()
    conn.close()
    print("EDT généré avec succès !")

if __name__ == "__main__":
    generate_exam_schedule()