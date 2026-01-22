from backend.db_connect import get_connection
from datetime import datetime, timedelta
import random

def generate_exam_schedule():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM examens")
    conn.commit()

    cur.execute("SELECT id FROM modules")
    modules = cur.fetchall()

    cur.execute("SELECT id, capacite FROM salles")
    salles = cur.fetchall()

    start_date = datetime.now()

    for module in modules:
        module_id = module[0]
        salle_id, capacite = random.choice(salles)
        date_exam = start_date

        cur.execute("INSERT INTO examens(module_id, salle_id, date_exam) VALUES (%s,%s,%s)",
                    (module_id, salle_id, date_exam.date()))

        start_date += timedelta(days=1)
        if start_date.weekday() == 4:
            start_date += timedelta(days=1)

    conn.commit()
    cur.close()
    conn.close()
    print("EDT généré avec succès !")
