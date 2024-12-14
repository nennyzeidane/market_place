CREATE DATABASE marketplace_universitaire;

USE marketplace_universitaire;

CREATE TABLE Etudiant (
    Matricule INT(11) AUTO_INCREMENT PRIMARY KEY,
    Non VARCHAR(255) NOT NULL,
    Prenom VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    Numero_du_telephone INT(255) NOT NULL
);

CREATE TABLE Annonce (
    id_annonce INT(11) AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    prix DECIMAL(10,2),
    date_publication DATE,
    Matricule INT(11),
    FOREIGN KEY (Matricule) REFERENCES Etudiant(Matricule)
);

CREATE TABLE Photo (
    id_photo INT(11) AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    id_annonce INT(11),
    FOREIGN KEY (id_annonce) REFERENCES Annonce(id_annonce)
);
