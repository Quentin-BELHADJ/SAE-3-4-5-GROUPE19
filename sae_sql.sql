DROP TABLE IF EXISTS liste_envie, commentaire,historique,note,ligne_panier,ligne_commande,commande,adresse, utilisateur, declinaison, lunette,sexe,fournisseur, marque, categorie_lunette, etat, couleur;

CREATE TABLE couleur(
   id_couleur INT AUTO_INCREMENT,
   libelle VARCHAR(50),
   code_couleur INT,
   PRIMARY KEY(id_couleur)
);

CREATE TABLE etat(
   id_etat INT AUTO_INCREMENT,
   libelle_etat VARCHAR(50),
   PRIMARY KEY(id_etat)
);

CREATE TABLE categorie_lunette(
   id_categorie_lunette INT AUTO_INCREMENT,
   libelle_categorie VARCHAR(50),
   PRIMARY KEY(id_categorie_lunette)
);

CREATE TABLE utilisateur(
   id_utilisateur INT AUTO_INCREMENT,
   login VARCHAR(50),
   email VARCHAR(50),
   nom VARCHAR(50),
   password VARCHAR(255),
   role VARCHAR(50),
   PRIMARY KEY(id_utilisateur)
);

CREATE TABLE adresse(
   id_adresse INT AUTO_INCREMENT,
   nom VARCHAR(50),
   rue VARCHAR(50),
   code_postal INT,
   ville VARCHAR(50),
   date_utilisation DATE,
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_adresse),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE marque(
   id_marque INT AUTO_INCREMENT,
   libelle_marque VARCHAR(50),
   PRIMARY KEY(id_marque)
);

CREATE TABLE fournisseur(
   id_fournisseur INT AUTO_INCREMENT,
   libelle_fournisseur VARCHAR(50),
   PRIMARY KEY(id_fournisseur)
);

CREATE TABLE sexe(
   id_sexe INT AUTO_INCREMENT,
   libelle VARCHAR(50),
   PRIMARY KEY(id_sexe)
);

CREATE TABLE lunette(
   id_lunette INT AUTO_INCREMENT,
   nom_lunette VARCHAR(50),
   disponible BOOLEAN,
   prix_lunette INT,
   description VARCHAR(50),
   image VARCHAR(50),
   id_categorie_lunette INT NOT NULL,
   id_fournisseur INT NOT NULL,
   id_marque INT NOT NULL,
   id_sexe INT NOT NULL,
   PRIMARY KEY(id_lunette),
   FOREIGN KEY(id_categorie_lunette) REFERENCES categorie_lunette(id_categorie_lunette),
   FOREIGN KEY(id_fournisseur) REFERENCES fournisseur(id_fournisseur),
   FOREIGN KEY(id_marque) REFERENCES marque(id_marque),
   FOREIGN KEY(id_sexe) REFERENCES sexe(id_sexe)
);

CREATE TABLE declinaison(
   id_declinaison INT AUTO_INCREMENT,
   stock INT,
   prix INT,
   image VARCHAR(50),
   id_couleur INT NOT NULL,
   id_lunette INT NOT NULL,
   PRIMARY KEY(id_declinaison),
   FOREIGN KEY(id_couleur) REFERENCES couleur(id_couleur),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette)
);

CREATE TABLE commande(
   id_commande INT AUTO_INCREMENT,
   date_achat DATE,
   id_etat INT NOT NULL,
   id_adresse INT NOT NULL,
   id_adresse_1 INT NOT NULL,
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_etat) REFERENCES etat(id_etat),
   FOREIGN KEY(id_adresse) REFERENCES adresse(id_adresse),
   FOREIGN KEY(id_adresse_1) REFERENCES adresse(id_adresse),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE ligne_commande(
   id_declinaison INT,
   id_commande INT,
   quantite INT,
   prix INT,
   PRIMARY KEY(id_declinaison, id_commande),
   FOREIGN KEY(id_declinaison) REFERENCES declinaison(id_declinaison),
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
);

CREATE TABLE ligne_panier(
   id_declinaison INT,
   id_utilisateur INT,
   quantite INT,
   PRIMARY KEY(id_declinaison, id_utilisateur),
   FOREIGN KEY(id_declinaison) REFERENCES declinaison(id_declinaison),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE note(
   id_lunette INT,
   id_utilisateur INT,
   note VARCHAR(50),
   PRIMARY KEY(id_lunette, id_utilisateur),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE historique(
   id_lunette INT,
   id_utilisateur INT,
   date_consultation VARCHAR(50),
   PRIMARY KEY(id_lunette, id_utilisateur, date_consultation),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE commentaire(
   id_lunette INT,
   id_utilisateur INT,
   date_publication DATE,
   commentaire VARCHAR(50),
   valider BOOLEAN,
   PRIMARY KEY(id_lunette, id_utilisateur, date_publication),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE liste_envie(
   id_lunette INT,
   id_utilisateur INT,
   date_update DATE,
   PRIMARY KEY(id_lunette, id_utilisateur, date_update),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

INSERT INTO couleur (libelle, code_couleur) VALUES
('Noir', 1),
('Blanc', 2),
('Rouge', 3),
('Vert', 4),
('Bleu', 5);

INSERT INTO categorie_lunette (id_categorie_lunette, libelle_categorie) VALUES
(1, 'Lunettes de soleil'),
(2, 'Lunettes de vue'),
(3, 'Lunettes de sport'),
(4, 'Lunettes pour enfant'),
(5, 'Lunettes de mode');

INSERT INTO marque (id_marque, libelle_marque) VALUES
(1, 'Ray-Ban'),
(2, 'Oakley'),
(3, 'Gucci'),
(4, 'Prada'),
(5, 'Dolce & Gabbana');

INSERT INTO fournisseur (id_fournisseur, libelle_fournisseur) VALUES
(1, 'Essilor'),
(2, 'Luxottica'),
(3, 'Marchon'),
(4, 'Safilo');
INSERT INTO etat(id_etat, libelle_etat) VALUES (1,'en attente'),
                                               (2,'expédié');

INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom) VALUES
(1,'admin','admin@admin.fr',
    'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
    'ROLE_admin','admin'),
(2,'client','client@client.fr',
    'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
    'ROLE_client','client'),
(3,'client2','client2@client2.fr',
    'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
    'ROLE_client','client2');

INSERT INTO sexe (libelle) VALUES
('H'),('F'),('HF');

INSERT INTO lunette (nom_lunette,description, prix_lunette, id_categorie_lunette, id_marque, id_fournisseur,id_sexe) VALUES
('Aviator','De belle lunette de soleil', 200.00, 1, 1, 1, 3),
('Round Metal','De belle lunette', 150.00, 2, 2, 2,3),
('Wayfarer','de belle lunette', 180.00, 3, 1, 1,3),
('Clubmaster','de belle lunette', 250.00, 1, 3, 3,3),
('Lunettes de sport','De belle lunette pour faire du sport', 300.00, 4, 4, 4, 3),
('Lunettes de vue rondes','De belle lunette avec des verres ronds', 120.00, 2, 2, 2, 3),
('Lunettes pour enfant','De belle lunettes pour enfant', 50.00, 4, 4, 2, 3),
('Lunettes de mode','De belle lunette pour etre à la mode', 250.00, 5, 5, 2, 3),
('Lunettes de vue rectangulaires','Des lunette rectangulaires, elles sont magnifique', 160.00, 1, 2, 1, 3),
('Steampunk','De belle lunette dans un univers SteamPunk', 100.00, 1, 2, 3, 3),
('Lunettes anti lumiere bleu','De belle lunettes anti lumière bleu', 90.00, 1, 2, 1, 3),
('Lunettes triangle','De belle lunette avec de verre triangulaire', 999.99, 1, 2, 1, 3),
('Lunettes de ski','De belle lunette pour faire du ski', 124.99, 1, 2, 1, 3),
('Lunettes de natation','De belle lunette pour nager', 20.99, 1, 3, 2, 3),
('Lunettes sans branches','De belle lunette sans branche', 199.99, 2, 4, 1, 3);

INSERT INTO declinaison(stock, prix, id_lunette, id_couleur)
VALUES
    (5, 200, 1, 4),
    (5, 150, 2, 1),
    (5, 180, 3, 1),
    (5, 250, 4, 1),
    (1, 300, 5, 1),
    (1, 300, 5, 2),
    (1, 300, 5, 3),
    (1, 300, 5, 4),
    (1, 300, 5, 5),
    (1, 120, 6, 1),
    (1, 120, 6, 2),
    (1, 120, 6, 3),
    (1, 120, 6, 4),
    (1, 120, 6, 5),
    (1, 50, 7, 1),
    (1, 50, 7, 2),
    (1, 50, 7, 3),
    (1, 50, 7, 4),
    (1, 50, 7, 5),
    (1, 250, 8, 1),
    (1, 250, 8, 2),
    (1, 250, 8, 3),
    (1, 250, 8, 4),
    (1, 250, 8, 5),
    (1, 160, 9, 1),
    (1, 160, 9, 2),
    (1, 160, 9, 3),
    (1, 160, 9, 4),
    (1, 160, 9, 5),
    (1, 100, 10, 1),
    (1, 100, 10, 2),
    (1, 100, 10, 3),
    (1, 100, 10, 4),
    (1, 100, 10, 5),
    (1, 90, 11, 1),
    (1, 90, 11, 2),
    (1, 90, 11, 3),
    (1, 90, 11, 4),
    (1, 90, 11, 5),
    (1, 999.99, 12, 1),
    (1, 999.99, 12, 2),
    (1, 999.99, 12, 3),
    (1, 999.99, 12, 4),
    (1, 999.99, 12, 5),
    (1, 124.99, 13, 1),
    (1, 124.99, 13, 2),
    (1, 124.99, 13, 3),
    (1, 124.99, 13, 4),
    (1, 124.99, 13, 5),
    (1, 20.99, 14, 1),
    (1, 20.99, 14, 2),
    (1, 20.99, 14, 3),
    (1, 20.99, 14, 4),
    (1, 20.99, 14, 5),
    (1, 199.99, 15, 1),
    (1, 199.99, 15, 2),
    (1, 199.99, 15, 3),
    (1, 199.99, 15, 4),
    (1, 199.99, 15, 5);

SELECT * FROM declinaison;

INSERT INTO adresse(nom,rue, code_postal,ville, id_utilisateur)
VALUES ("NOM prénom", "1 rue de machin" ,"90000", "Belfort",2),
    ("BELHADJ Quentin", "9 rue des maraîchers" ,"90000", "Belfort",2);

INSERT INTO ligne_panier VALUES (1,2,1),
                                (2,2,2),
                                (35,2,1),
                                (36,2,1);