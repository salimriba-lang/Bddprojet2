from db_connect import get_connection
from datetime import datetime, timedelta
import random

def generate_exam_schedule():
    conn = get_connection()
    cur = conn.cursor()

    # Supprimer les examens existants pour régénérer
    cur.execute("DELETE FROM examens")
    cur.execute("DELETE FROM surveillances")
    conn.commit()

    # Récupérer tous les modules et salles
    cur.execute("SELECT id FROM modules")
    modules = cur.fetchall()

    cur.execute("SELECT id, capacite FROM salles")
    salles = cur.fetchall()

    # Récupérer tous les professeurs depuis la DB
    cur.execute("SELECT id FROM professeurs")
    profs = [p[0] for p in cur.fetchall()]

    # Simuler les étudiants en mémoire (13 000)
    n_students_sim = 13000
    simulated_students = [f"Etudiant{i}" for i in range(n_students_sim)]

    start_date = datetime.now()  # début de la génération

    for module in modules:
        module_id = module[0]
        salle_id, capacite = random.choice(salles)
        date_exam = start_date

        # Calculer un nombre d'étudiants aléatoire pour le module
        nb_students_for_module = random.randint(30, 200)

        # Vérifier que la salle peut contenir les étudiants simulés
        if nb_students_for_module > capacite:
            # Choisir une autre salle si nécessaire
            possible_salles = [s for s in salles if s[1] >= nb_students_for_module]
            if possible_salles:
                salle_id, capacite = random.choice(possible_salles)
            else:
                # Si aucune salle ne suffit, prendre la plus grande
                salle_id, capacite = max(salles, key=lambda s: s[1])

        # Insérer l'examen
        cur.execute(
            "INSERT INTO examens(module_id, salle_id, date_exam) VALUES (%s,%s,%s) RETURNING id",
            (module_id, salle_id, date_exam.date())
        )
        examen_id = cur.fetchone()[0]

        # Assigner 1 à 3 profs aléatoires pour surveiller l'examen
        for _ in range(random.randint(1,3)):
            professeur_id = random.choice(profs)
            cur.execute(
                "INSERT INTO surveillances(examen_id, professeur_id) VALUES (%s,%s)",
                (examen_id, professeur_id)
            )

        # Passer au jour suivant
        start_date += timedelta(days=1)
        if start_date.weekday() == 4:  # Skip vendredi
            start_date += timedelta(days=1)

    conn.commit()
    cur.close()
    conn.close()
    print("EDT généré avec succès !")

if __name__ == "__main__":
    generate_exam_schedule()
