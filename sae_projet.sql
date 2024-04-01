DROP TABLE IF EXISTS liste_envie, commentaire,historique,note,ligne_panier,ligne_commande,commande,adresse, utilisateur, declinaison, lunette,sexe,fournisseur, marque, categorie_lunette, etat, couleur;

CREATE TABLE couleur(
   id_couleur INT AUTO_INCREMENT,
   libelle VARCHAR(50),
   code_couleur INT,
   PRIMARY KEY(id_couleur)
)DEFAULT CHARSET=utf8mb4;

CREATE TABLE etat(
   id_etat INT AUTO_INCREMENT,
   libelle_etat VARCHAR(50),
   PRIMARY KEY(id_etat)
)DEFAULT CHARSET=utf8mb4;

CREATE TABLE categorie_lunette(
   id_categorie_lunette INT AUTO_INCREMENT,
   libelle_categorie VARCHAR(50),
   PRIMARY KEY(id_categorie_lunette)
)DEFAULT CHARSET=utf8mb4;

CREATE TABLE utilisateur(
   id_utilisateur INT AUTO_INCREMENT,
   login VARCHAR(50),
   email VARCHAR(50),
   nom VARCHAR(50),
   password VARCHAR(255),
   role VARCHAR(50),
   PRIMARY KEY(id_utilisateur)
)DEFAULT CHARSET=utf8mb4;

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
)DEFAULT CHARSET=utf8mb4;

CREATE TABLE marque(
   id_marque INT AUTO_INCREMENT,
   libelle_marque VARCHAR(50),
   PRIMARY KEY(id_marque)
)DEFAULT CHARSET=utf8mb4;

CREATE TABLE fournisseur(
   id_fournisseur INT AUTO_INCREMENT,
   libelle_fournisseur VARCHAR(50),
   PRIMARY KEY(id_fournisseur)
)DEFAULT CHARSET=utf8mb4;

CREATE TABLE sexe(
   id_sexe INT AUTO_INCREMENT,
   libelle VARCHAR(50),
   PRIMARY KEY(id_sexe)
)DEFAULT CHARSET=utf8mb4;

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
   nb_consultation INT DEFAULT 0,
   PRIMARY KEY(id_lunette),
   FOREIGN KEY(id_categorie_lunette) REFERENCES categorie_lunette(id_categorie_lunette),
   FOREIGN KEY(id_fournisseur) REFERENCES fournisseur(id_fournisseur),
   FOREIGN KEY(id_marque) REFERENCES marque(id_marque),
   FOREIGN KEY(id_sexe) REFERENCES sexe(id_sexe)
)DEFAULT CHARSET=utf8mb4;

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
)DEFAULT CHARSET=utf8mb4;

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
)DEFAULT CHARSET=utf8mb4;

CREATE TABLE ligne_commande(
   id_declinaison INT,
   id_commande INT,
   quantite INT,
   prix INT,
   PRIMARY KEY(id_declinaison, id_commande),
   FOREIGN KEY(id_declinaison) REFERENCES declinaison(id_declinaison),
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
)DEFAULT CHARSET=utf8mb4;

CREATE TABLE ligne_panier(
   id_declinaison INT,
   id_utilisateur INT,
   quantite INT,
   PRIMARY KEY(id_declinaison, id_utilisateur),
   FOREIGN KEY(id_declinaison) REFERENCES declinaison(id_declinaison),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
)DEFAULT CHARSET=utf8mb4;

CREATE TABLE note(
   id_lunette INT,
   id_utilisateur INT,
   note VARCHAR(50),
   PRIMARY KEY(id_lunette, id_utilisateur),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
)DEFAULT CHARSET=utf8mb4;

CREATE TABLE historique(
   id_lunette INT,
   id_utilisateur INT,
   date_consultation DATETIME,
   PRIMARY KEY(id_lunette, id_utilisateur, date_consultation),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
)DEFAULT CHARSET=utf8mb4;

CREATE TABLE commentaire(
   id_lunette INT,
   id_utilisateur INT,
   date_publication DATETIME,
   commentaire VARCHAR(250),
   valider BOOLEAN,
   PRIMARY KEY(id_lunette, id_utilisateur, date_publication),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
)DEFAULT CHARSET=utf8mb4;

CREATE TABLE liste_envie(
   id_lunette INT,
   id_utilisateur INT,
   date_update DATETIME,
   PRIMARY KEY(id_lunette, id_utilisateur, date_update),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
)DEFAULT CHARSET=utf8mb4;

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

INSERT INTO utilisateur(id_utilisateur,login,email,nom,password,role) VALUES
 (1 , 'admin'   , 'admin@admin.fr','admin', 'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf' , 'ROLE_admin' ),
(2 , 'client'  , 'client@client.fr' , 'client'  , 'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d' , 'ROLE_client' ),
(3 , 'client2' , 'client2@client2.fr', 'client2' , 'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422' , 'ROLE_client' ),
(4 , 'client3' , 'client3@gmail.com', 'client3' , 'sha256$EtzORFk4cs3J4a6r$4f045536fc178adf879fb29af831ac54065212df30d478c54ac355b25e657027' , 'ROLE_client' ),
(5 , 'client4' , 'client4' , 'client4' , 'sha256$n4dPDiS2gOdrhgQS$a713b4540dbf5d8e20a720299f6c0e99c6f64782bf73adef9b761a171a134359' , 'ROLE_client' ),
(6 , 'client5' , 'client5'  , 'client5' , 'sha256$BpkQtxQVANbYZUbg$75fb773c680a3922def295e7ae5211c90ceed29d2f93e46ada6118cfc2a98f56' , 'ROLE_client' ),
(7 , 'client6' , 'client6' , 'client6' , 'sha256$5rUv6eOcFESZ6t0W$ed1dd6d175d1090ea5325db33534b1e28694d8dc550fc2605affaade4133886c' , 'ROLE_client' );

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
VALUES ('NOM prénom', '1 rue de machin' ,90000, 'Belfort',2),
    ('BELHADJ Quentin', '9 rue des maraîchers' ,90000, 'Belfort',2);

INSERT INTO ligne_panier VALUES (1,2,1),
                                (2,2,2),
                                (35,2,1),
                                (36,2,1);

-- Commentaires pour l'utilisateur 2 (client)
INSERT INTO commentaire (id_lunette, id_utilisateur, date_publication, commentaire, valider) VALUES
(1, 2, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Ces lunettes sont vraiment géniales !', 0),
(2, 2, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Je suis déçu de la qualité des lunettes.', 0),
(3, 2, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Excellent rapport qualité-prix.', 0);

-- Commentaires pour l'utilisateur 3 (client2)
INSERT INTO commentaire (id_lunette, id_utilisateur, date_publication, commentaire, valider) VALUES
(1, 3, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'J\'ai adoré ces lunettes, elles sont superbes !', 0),
(2, 3, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Très confortables, je recommande.', 0),
(4, 3, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Le design est vraiment original.', 0);

-- Commentaires pour l'utilisateur 4 (client3)
INSERT INTO commentaire (id_lunette, id_utilisateur, date_publication, commentaire, valider) VALUES
(2, 4, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Je ne suis pas satisfait de cet achat.', 0),
(3, 4, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Les lunettes sont arrivées rapidement, merci !', 0),
(5, 4, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Je les ai offertes en cadeau, la personne était ravie.', 0);

-- Commentaires pour l'utilisateur 5 (client4)
INSERT INTO commentaire (id_lunette, id_utilisateur, date_publication, commentaire, valider) VALUES
(1, 5, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Très bon produit, conforme à la description.', 0),
(4, 5, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Lunettes de qualité, je recommande.', 0),
(6, 5, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Service client réactif et professionnel.', 0);

-- Commentaires pour l'utilisateur 6 (client5)
INSERT INTO commentaire (id_lunette, id_utilisateur, date_publication, commentaire, valider) VALUES
(3, 6, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Les lunettes sont un peu fragiles à mon goût.', 0),
(5, 6, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Je suis satisfait de mon achat, merci !', 0),
(7, 6, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Je les ai reçues en parfait état.', 0);

-- Commentaires pour l'utilisateur 7 (client6)
INSERT INTO commentaire (id_lunette, id_utilisateur, date_publication, commentaire, valider) VALUES
(4, 7, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Les lunettes sont conformes à mes attentes.', 0),
(6, 7, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Je les ai commandées pour un événement, elles sont parfaites !', 0),
(8, 7, DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 30) DAY), 'Livraison rapide et emballage soigné.', 0);

INSERT INTO note (id_lunette, id_utilisateur, note)
SELECT c.id_lunette, c.id_utilisateur, ROUND(RAND() * 3) + 2
FROM commentaire c
GROUP BY c.id_lunette, c.id_utilisateur
HAVING COUNT(*) >= 1;