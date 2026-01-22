CREATE OR REPLACE FUNCTION check_etudiant_exam()
RETURNS trigger AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM examens e
        JOIN inscriptions i1 ON i1.module_id = e.module_id
        JOIN inscriptions i2 ON i2.etudiant_id = i1.etudiant_id
        WHERE i2.module_id = NEW.module_id
        AND e.date_exam = NEW.date_exam
    ) THEN
        RAISE EXCEPTION
        'Conflit : un étudiant a déjà un examen le %', NEW.date_exam;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_exam_etudiant
BEFORE INSERT ON examens
FOR EACH ROW
EXECUTE FUNCTION check_etudiant_exam();


-- ============================================
-- Trigger : capacité de la salle respectée
-- ============================================

CREATE OR REPLACE FUNCTION check_salle_capacite()
RETURNS trigger AS $$
DECLARE
    nb_etudiants INT;
    cap_salle INT;
BEGIN
    SELECT COUNT(*)
    INTO nb_etudiants
    FROM inscriptions
    WHERE module_id = NEW.module_id;

    SELECT capacite
    INTO cap_salle
    FROM salles
    WHERE id = NEW.salle_id;

    IF nb_etudiants > cap_salle THEN
        RAISE EXCEPTION
        'Capacité insuffisante : % étudiants pour % places',
        nb_etudiants, cap_salle;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_salle_capacite
BEFORE INSERT ON examens
FOR EACH ROW
EXECUTE FUNCTION check_salle_capacite();


-- ============================================
-- Trigger : un professeur max 3 examens / jour
-- ============================================

CREATE OR REPLACE FUNCTION check_prof_exam()
RETURNS trigger AS $$
DECLARE
    nb_exam INT;
BEGIN
    SELECT COUNT(*)
    INTO nb_exam
    FROM surveillances s
    JOIN examens e ON e.id = s.examen_id
    JOIN examens e2 ON e2.id = NEW.examen_id
    WHERE s.professeur_id = NEW.professeur_id
    AND e.date_exam = e2.date_exam;

    IF nb_exam >= 3 THEN
        RAISE EXCEPTION
        'Conflit : professeur % a déjà 3 examens le %',
        NEW.professeur_id, (SELECT date_exam FROM examens WHERE id = NEW.examen_id);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_prof_exam
BEFORE INSERT ON surveillances
FOR EACH ROW
EXECUTE FUNCTION check_prof_exam();
