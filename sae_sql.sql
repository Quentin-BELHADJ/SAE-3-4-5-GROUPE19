DROP TABLE IF EXISTS est_de;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS lunette;
DROP TABLE IF EXISTS fournisseur;
DROP TABLE IF EXISTS marque;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS categorie;
DROP TABLE IF EXISTS utilisateur;

CREATE TABLE couleur(
   id_couleur INT AUTO_INCREMENT,
   libelle_couleur VARCHAR(50),
   PRIMARY KEY(id_couleur)
);

CREATE TABLE categorie(
   id_categorie INT AUTO_INCREMENT,
   libelle_categorie VARCHAR(50),
   PRIMARY KEY(id_categorie)
);

CREATE TABLE utilisateur(
   id_utilisateur INT AUTO_INCREMENT,
   login VARCHAR(50),
   email VARCHAR(255),
   nom VARCHAR(255),
   password VARCHAR(255),
   role VARCHAR(255),
   est_actif SMALLINT,
   PRIMARY KEY(id_utilisateur)
);

CREATE TABLE etat(
   id_etat INT AUTO_INCREMENT,
   libelle_etat VARCHAR(40),
   PRIMARY KEY(id_etat)
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

CREATE TABLE lunette(
   id_lunette INT AUTO_INCREMENT,
   libelle_lunette VARCHAR(255),
   sexe VARCHAR(31),
   indice_protection INT,
   taille_monture INT,
   prix_lunette DECIMAL(12,2),
   couleur_id INT,
   categorie_id INT,
   id_marque INT NOT NULL,
   id_fournisseur INT NOT NULL,
   id_categorie INT NOT NULL,
   id_couleur INT NOT NULL,
   PRIMARY KEY(id_lunette),
   FOREIGN KEY(id_marque) REFERENCES marque(id_marque),
   FOREIGN KEY(id_fournisseur) REFERENCES fournisseur(id_fournisseur),
   FOREIGN KEY(id_categorie) REFERENCES categorie(id_categorie),
   FOREIGN KEY(id_couleur) REFERENCES couleur(id_couleur)
);

CREATE TABLE commande(
   id_commande INT AUTO_INCREMENT,
   date_achat DATE,
   id_etat INT NOT NULL,
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_etat) REFERENCES etat(id_etat),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE ligne_commande(
   id_lunette INT,
   id_commande INT,
   prix DECIMAL(12,2),
   quantite INT,
   PRIMARY KEY(id_lunette, id_commande),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette),
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
);

CREATE TABLE ligne_panier(
   id_lunette INT,
   id_utilisateur INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(id_lunette, id_utilisateur),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);



INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(1,'admin','admin@admin.fr',
    'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
    'ROLE_admin','admin','1'),
(2,'client','client@client.fr',
    'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
    'ROLE_client','client','1'),
(3,'client2','client2@client2.fr',
    'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
    'ROLE_client','client2','1');

-- Insertion de données dans la table couleur
INSERT INTO couleur (id_couleur, libelle_couleur) VALUES
(1, 'Noir'),
(2, 'Blanc'),
(3, 'Rouge'),
(4, 'Bleu'),
(5, 'Vert');

-- Insertion de données dans la table categorie
INSERT INTO categorie (id_categorie, libelle_categorie) VALUES
(1, 'Lunettes de soleil'),
(2, 'Lunettes de vue'),
(3, 'Lunettes de sport'),
(4, 'Lunettes pour enfant'),
(5, 'Lunettes de mode');

-- Insertion de données dans la table marque
INSERT INTO marque (id_marque, libelle_marque) VALUES
(1, 'Ray-Ban'),
(2, 'Oakley'),
(3, 'Gucci'),
(4, 'Prada'),
(5, 'Dolce & Gabbana');

-- Insertion de données dans la table fournisseur
INSERT INTO fournisseur (id_fournisseur, libelle_fournisseur) VALUES
(1, 'Essilor'),
(2, 'Luxottica'),
(3, 'Marchon'),
(4, 'Safilo');

-- Insertion de données dans la table lunette
INSERT INTO lunette (id_lunette, libelle_lunette, prix_lunette, id_couleur, id_categorie, id_marque, id_fournisseur) VALUES
(1, 'Aviator', 200.00, 1, 1, 1, 1),
(2, 'Round Metal', 150.00, 2, 2, 2, 2),
(3, 'Wayfarer', 180.00, 3, 1, 1, 3),
(4, 'Clubmaster', 250.00, 1, 3, 3, 4),
(5, 'Lunettes de sport', 300.00, 4, 4, 5, 1),
(6, 'Lunettes de mode', 400.00, 5, 5, 4, 2),
(7, 'Lunettes de soleil aviateur noires', 150.00, 1, 1, 1, 1),
(8, 'Lunettes de vue rondes blanches', 120.00, 2, 2, 2, 2),
(9, 'Lunettes de sport rouges', 350.00, 3, 4, 5, 3),
(10, 'Lunettes pour enfant bleues', 50.00, 4, 4, 2, 1),
(11, 'Lunettes de mode vertes', 250.00, 5, 5, 2, 2),
(12, 'Lunettes de soleil aviateur rouges', 180.00, 3, 1, 1, 3),
(13, 'Lunettes de vue rectangulaires noires', 160.00, 1, 2, 1, 4),
(14, 'Lunettes de sport bleues', 400.00, 4, 4, 4, 1),
(15, 'Lunettes pour enfant rouges', 70.00, 3, 4, 3, 2),
(16, 'Lunettes de mode jaunes', 300.00, 5, 5, 5, 4);
