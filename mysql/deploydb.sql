-- Creation de la base de données --
CREATE DATABASE IF NOT EXISTS TP2020_MORVAL;

-- Création d'un user à notre nom et attribution de tout les privilèges--
USE TP2020_MORVAL;
CREATE USER IF NOT EXISTS 'neth'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON moreau.* to 'neth'@'%';

-- Création de la table des personnes --
USE TP2020_MORVAL;
DROP TABLE IF EXISTS salaire;
CREATE TABLE salaire
(
    nom VARCHAR(20),
    salaireORE int,
    salairePHE VARCHAR(2000)
);
GO

-- Insertion des valeurs automatiquement --
INSERT INTO salaire (nom, salaireORE, salairePHE)
VALUES 
-- ANSSI RECOMMANDATIONS FOR PASSWORD plainSalaire = 2341 for all--
('DUPONT','163354826','{"public_key": 2161831391, "ciphertext": "2803573453228191695", "exponent": 0}'),
('MOREAU','163354826','{"public_key": 2161831391, "ciphertext": "2803573453228191695", "exponent": 0}'),
('VALLET','163354826','{"public_key": 2161831391, "ciphertext": "2803573453228191695", "exponent": 0}'),
('SUZIE','163354826','{"public_key": 2161831391, "ciphertext": "2803573453228191695", "exponent": 0}'),
('TEOUX','163354826','{"public_key": 2161831391, "ciphertext": "2803573453228191695", "exponent": 0}'),
('KOMODO','163354826','{"public_key": 2161831391, "ciphertext": "2803573453228191695", "exponent": 0}'),
('GINA','163354826','{"public_key": 2161831391, "ciphertext": "2803573453228191695", "exponent": 0}');
GO

