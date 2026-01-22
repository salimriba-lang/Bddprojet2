CREATE DATABASE IF NOT EXISTS bddprojet;
USE bddprojet;

CREATE TABLE departements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE formations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(150),
    dept_id INT,
    nb_modules INT,
    niveau VARCHAR(10),
    FOREIGN KEY (dept_id) REFERENCES departements(id)
);

CREATE TABLE modules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(150),
    credits INT,
    formation_id INT,
    FOREIGN KEY (formation_id) REFERENCES formations(id)
);

CREATE TABLE etudiants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    formation_id INT,
    promo INT,
    FOREIGN KEY (formation_id) REFERENCES formations(id)
);

CREATE TABLE professeurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100),
    dept_id INT,
    specialite VARCHAR(150),
    FOREIGN KEY (dept_id) REFERENCES departements(id)
);

CREATE TABLE salles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50),
    capacite INT,
    type VARCHAR(30),
    batiment VARCHAR(50)
);

CREATE TABLE examens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    module_id INT,
    salle_id INT,
    date_exam DATE,
    heure_debut TIME DEFAULT '08:00:00',
    duree TIME DEFAULT '01:30:00',
    FOREIGN KEY (module_id) REFERENCES modules(id),
    FOREIGN KEY (salle_id) REFERENCES salles(id)
);

CREATE TABLE utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50),
    role VARCHAR(20)
);
