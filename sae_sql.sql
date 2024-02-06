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

CREATE TABLE IF NOT EXISTS couleur(
   id_couleur INT AUTO_INCREMENT,
   libelle_couleur VARCHAR(50),
   PRIMARY KEY(id_couleur)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE IF NOT EXISTS categorie(
   id_categorie INT AUTO_INCREMENT,
   libelle_categorie VARCHAR(50),
   PRIMARY KEY(id_categorie)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE IF NOT EXISTS utilisateur(
   id_utilisateur INT AUTO_INCREMENT,
   login VARCHAR(50),
   email VARCHAR(255),
   nom VARCHAR(255),
   password VARCHAR(255),
   role VARCHAR(255),
   est_actif SMALLINT,
   PRIMARY KEY(id_utilisateur)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE IF NOT EXISTS etat(
   id_etat INT AUTO_INCREMENT,
   libelle_etat VARCHAR(40),
   PRIMARY KEY(id_etat)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE IF NOT EXISTS marque(
   id_marque INT AUTO_INCREMENT,
   libelle_marque VARCHAR(50),
   PRIMARY KEY(id_marque)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE IF NOT EXISTS fournisseur(
   id_fournisseur INT AUTO_INCREMENT,
   libelle_fournisseur VARCHAR(50),
   PRIMARY KEY(id_fournisseur)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE IF NOT EXISTS lunette(
   id_lunette INT AUTO_INCREMENT,
   libelle_lunette VARCHAR(255),
   sexe VARCHAR(31),
   indice_protection INT,
   taille_monture INT,
   prix_lunette DECIMAL(12,2),
   marque_id INT NOT NULL,
   fournisseur_id INT NOT NULL,
   categorie_id INT NOT NULL,
   couleur_id INT NOT NULL,
   PRIMARY KEY(id_lunette),
   FOREIGN KEY(marque_id) REFERENCES marque(id_marque),
   FOREIGN KEY(fournisseur_id) REFERENCES fournisseur(id_fournisseur),
   FOREIGN KEY(categorie_id) REFERENCES categorie(id_categorie),
   FOREIGN KEY(couleur_id) REFERENCES couleur(id_couleur)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE IF NOT EXISTS commande(
   id_commande INT AUTO_INCREMENT,
   date_achat DATE,
   etat_id INT NOT NULL,
   utilisateur_id INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(etat_id) REFERENCES etat(id_etat),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE IF NOT EXISTS ligne_commande(
   lunette_id INT,
   commande_id INT,
   prix DECIMAL(12,2),
   quantite INT,
   PRIMARY KEY(lunette_id, commande_id),
   FOREIGN KEY(lunette_id) REFERENCES lunette(id_lunette),
   FOREIGN KEY(commande_id) REFERENCES commande(id_commande)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE IF NOT EXISTS ligne_panier(
   lunette_id INT,
   utilisateur_id INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(lunette_id, utilisateur_id),
   FOREIGN KEY(lunette_id) REFERENCES lunette(id_lunette),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)
)DEFAULT CHARSET utf8mb4;



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
INSERT INTO lunette (id_lunette, libelle_lunette, prix_lunette, couleur_id, categorie_id, marque_id, fournisseur_id) VALUES
(1, 'Aviator', 200.00, 1, 1, 1, 1),
(2, 'Round Metal', 150.00, 2, 2, 2, 2),
(3, 'Wayfarer', 180.00, 3, 1, 1, 3),
(4, 'Clubmaster', 250.00, 1, 3, 3, 4),
(5, 'Lunettes de sport', 300.00, 4, 4, 5, 1),
(6, 'Lunettes de vue rondes', 120.00, 2, 2, 2, 2),
(7, 'Lunettes pour enfant', 50.00, 4, 4, 2, 1),
(8, 'Lunettes de mode', 250.00, 5, 5, 2, 2),
(9, 'Lunettes de vue rectangulaires', 160.00, 1, 2, 1, 4),
(10, 'Steampunk', 100.00, 1, 2, 3, 3),
(11, 'Lunettes anti lumiere bleu', 90.00, 1, 2, 1, 4),
(12, 'Lunettes triangle', 999.99, 1, 2, 1, 4),
(13, 'Lunettes de ski', 124.99, 1, 2, 1, 4),
(14, 'Lunettes de natation', 20.99, 1, 3, 2, 1),
(15, 'Lunettes sans branches', 199.99, 2, 4, 1, 4);

INSERT INTO etat(id_etat, libelle_etat) VALUES (1,'en attente'),
                                               (2,'expédié'),
                                               (3,'validé'),
                                               (4,'confirmé');


INSERT INTO ligne_panier(lunette_id,utilisateur_id,quantite,date_ajout)
VALUES (1,2,1,"2024-01-01"), (2,2,2,"2024-01-01")