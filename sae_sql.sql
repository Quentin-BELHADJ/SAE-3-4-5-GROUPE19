DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS lunette;
DROP TABLE IF EXISTS fournisseur;
DROP TABLE IF EXISTS marque;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS categorie;
DROP TABLE IF EXISTS couleur;

CREATE TABLE couleur(
   id_couleur INT,
   libelle_couleur VARCHAR(31),
   PRIMARY KEY(id_couleur)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE categorie(
   id_categorie INT,
   libelle_categorie VARCHAR(31),
   PRIMARY KEY(id_categorie)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE utilisateur (
    id_utilisateur int PRIMARY KEY,
    login VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    est_actif tinyint,
    nom VARCHAR(255),
    email VARCHAR(25)) DEFAULT CHARSET utf8mb4;

CREATE TABLE etat(
   id_etat INT,
   libelle_etat VARCHAR(31),
   PRIMARY KEY(id_etat)
)DEFAULT CHARSET utf8mb4;


CREATE TABLE marque(
   id_marque INT,
   libelle_marque VARCHAR(255),
   PRIMARY KEY(id_marque)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE fournisseur(
   id_fournisseur INT,
   libelle_fournisseur VARCHAR(255),
   PRIMARY KEY(id_fournisseur)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE lunette(
   id_lunette INT,
   nom_lunette VARCHAR(31),
   sexe VARCHAR(31),
   indice_protection INT,
   taille_monture INT,
   prix_lunette DECIMAL(12,2),
   couleur_id INT,
   categorie_id INT,
   id_marque INT NOT NULL,
   id_fournisseur INT NOT NULL,
   id_categorie INT NOT NULL,
   PRIMARY KEY(id_lunette),
   FOREIGN KEY(couleur_id) REFERENCES couleur(id_couleur),
   FOREIGN KEY(id_marque) REFERENCES marque(id_marque),
   FOREIGN KEY(id_fournisseur) REFERENCES fournisseur(id_fournisseur),
   FOREIGN KEY(id_categorie) REFERENCES categorie(id_categorie)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE commande(
   id_commande INT,
   date_achat DATE,
   id_etat INT NOT NULL,
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_etat) REFERENCES Etat(id_etat),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE ligne_commande(
   id_lunette INT,
   id_commande INT,
   prix DECIMAL(12,2),
   quantite INT,
   PRIMARY KEY(id_lunette, id_commande),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette),
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE ligne_panier(
   id_lunette INT,
   id_utilisateur INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(id_lunette, id_utilisateur),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
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

INSERT INTO etat(id_etat, libelle_etat) VALUES (1,'en attente'),
                                               (2,'expédié'),
                                               (3,'validé'),
                                               (4,'confirmé');