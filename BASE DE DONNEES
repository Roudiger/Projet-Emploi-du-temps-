 -- Créer la base de données projetinfo
CREATE DATABASE IF NOT EXISTS projetinfo;

-- Utiliser la base de données projetinfo
USE projetinfo;





-- Table des professeurs
CREATE TABLE IF NOT EXISTS Professeurs (
    ID_Professeur INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(255),
    Prenom VARCHAR(255)
);
-- Table des matières
CREATE TABLE IF NOT EXISTS Matieres (
    ID_Matiere INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(255),
    ID_Professeur INT,
    Nb_Cours INT,
    Duree VARCHAR(10), -- Modification de la colonne Duree pour stocker des durées sous forme de chaînes de caractères
    FOREIGN KEY (ID_Professeur) REFERENCES Professeurs(ID_Professeur)
);


-- Table des salles
CREATE TABLE IF NOT EXISTS Salles (
    ID_Salle INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(255),
    Capacite INT
);

-- Table des disponibilités des professeurs
CREATE TABLE IF NOT EXISTS Disponibilites (
    ID_Disponibilite INT AUTO_INCREMENT PRIMARY KEY,
    ID_Professeur INT,
    JourSemaine VARCHAR(255),
    HeureDebut TIME,
    HeureFin TIME,
    FOREIGN KEY (ID_Professeur) REFERENCES Professeurs(ID_Professeur)
);

-- Table des classes
CREATE TABLE IF NOT EXISTS Classes (
    ID_Classe INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(255)
);

-- Table des élèves
CREATE TABLE IF NOT EXISTS Eleves (
    ID_Eleve INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(255),
    Prenom VARCHAR(255),
    ID_Classe INT,
    FOREIGN KEY (ID_Classe) REFERENCES Classes(ID_Classe)
);

-- Table des cours étudiants
CREATE TABLE IF NOT EXISTS Cours_Etudiants (
    ID_Cours INT AUTO_INCREMENT PRIMARY KEY,
    ID_Professeur INT,
    ID_Matiere INT,
    ID_Salle INT,
    JourSemaine VARCHAR(255),
    HeureDebut TIME,
    HeureFin TIME,
    FOREIGN KEY (ID_Professeur) REFERENCES Professeurs(ID_Professeur),
    FOREIGN KEY (ID_Matiere) REFERENCES Matieres(ID_Matiere),
    FOREIGN KEY (ID_Salle) REFERENCES Salles(ID_Salle)
);

-- Table de liaison entre Classes et Cours_Etudiants
CREATE TABLE IF NOT EXISTS Cours_Classe (
    ID_Cours INT,
    ID_Classe INT,
    FOREIGN KEY (ID_Cours) REFERENCES Cours_Etudiants(ID_Cours),
    FOREIGN KEY (ID_Classe) REFERENCES Classes(ID_Classe)
);

-- Table des disponibilités des salles
CREATE TABLE IF NOT EXISTS Disponibilites_salle (
    ID_Disponibilite INT AUTO_INCREMENT PRIMARY KEY,
    ID_Salle INT,
    JourSemaine VARCHAR(10),
    HeureDebut TIME,
    HeureFin TIME,
    FOREIGN KEY (ID_Salle) REFERENCES Salles(ID_Salle)
);
