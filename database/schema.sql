-- départements
CREATE TABLE departements (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL
);

-- formations (Licence 3 ans + Master 2 ans)
CREATE TABLE formations (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    dept_id INT REFERENCES departements(id),
    nb_modules INT CHECK (nb_modules BETWEEN 6 AND 9),
    niveau VARCHAR(10) NOT NULL
);

-- modules
CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    credits INT CHECK (credits > 0),
    formation_id INT REFERENCES formations(id),
    pre_req_id INT REFERENCES modules(id)
);

-- étudiants
CREATE TABLE etudiants (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    formation_id INT REFERENCES formations(id),
    promo INT
);

-- inscriptions étudiants
CREATE TABLE inscriptions (
    etudiant_id INT REFERENCES etudiants(id),
    module_id INT REFERENCES modules(id),
    note NUMERIC(4,2),
    PRIMARY KEY (etudiant_id, module_id)
);

-- professeurs
CREATE TABLE professeurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100),
    dept_id INT REFERENCES departements(id),
    specialite VARCHAR(150)
);

-- salles
CREATE TABLE salles (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50),
    capacite INT CHECK (capacite <= 20),
    type VARCHAR(30),
    batiment VARCHAR(50)
);

-- examens
CREATE TABLE examens (
    id SERIAL PRIMARY KEY,
    module_id INT REFERENCES modules(id),
    salle_id INT REFERENCES salles(id),
    date_exam DATE NOT NULL,
    heure_debut TIME DEFAULT '08:00',
    duree INTERVAL DEFAULT '1 hour 30 minutes',
    CHECK (EXTRACT(DOW FROM date_exam) <> 5)
);

-- surveillances
CREATE TABLE surveillances (
    examen_id INT REFERENCES examens(id),
    professeur_id INT REFERENCES professeurs(id),
    PRIMARY KEY (examen_id, professeur_id)
);

-- utilisateurs pour login (doyen, admin, chefdep, prof, etudiant)
CREATE TABLE utilisateurs (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    role VARCHAR(20) NOT NULL
);
