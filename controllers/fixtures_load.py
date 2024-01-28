#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                          template_folder='templates')


@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    sql = '''DROP TABLE IF EXISTS ligne_panier,ligne_commande,commande,lunette,fournisseur,marque,etat,couleur,categorie,utilisateur;'''
    mycursor.execute(sql)

    sql = ''' 
            CREATE TABLE IF NOT EXISTS couleur(
   id_couleur INT,
   libelle_couleur VARCHAR(31),
   PRIMARY KEY(id_couleur)
)DEFAULT CHARSET utf8mb4;'''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE IF NOT EXISTS categorie(
       id_categorie INT,
       libelle_categorie VARCHAR(31),
       PRIMARY KEY(id_categorie)
    )DEFAULT CHARSET utf8mb4;
        '''

    mycursor.execute(sql)
    sql = '''CREATE TABLE IF NOT EXISTS utilisateur (
        id_utilisateur INT NOT NULL AUTO_INCREMENT,
       login VARCHAR(50),
       email VARCHAR(255),
       nom VARCHAR(255),
       password VARCHAR(255),
       role VARCHAR(255),
       est_actif SMALLINT,
       PRIMARY KEY(id_utilisateur)
    )DEFAULT CHARSET utf8mb4;
    '''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS etat(
   id_etat INT AUTO_INCREMENT,
   libelle_etat VARCHAR(40),
   PRIMARY KEY(id_etat)
    )DEFAULT CHARSET utf8mb4;'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS marque(
   id_marque INT AUTO_INCREMENT,
   libelle_marque VARCHAR(50),
   PRIMARY KEY(id_marque)
    )DEFAULT CHARSET utf8mb4;'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS fournisseur(
   id_fournisseur INT AUTO_INCREMENT,
   libelle_fournisseur VARCHAR(50),
   PRIMARY KEY(id_fournisseur)
    )DEFAULT CHARSET utf8mb4;'''
    mycursor.execute(sql)

    sql = ''' 
        CREATE TABLE IF NOT EXISTS lunette(
       id_lunette INT,
       libelle_lunette VARCHAR(255),
       sexe VARCHAR(31),
       indice_protection INT,
       taille_monture INT,
       prix_lunette DECIMAL(12,2),
       id_couleur INT,
       categorie_id INT,
       id_marque INT NOT NULL,
       id_fournisseur INT NOT NULL,
       id_categorie INT NOT NULL,
       PRIMARY KEY(id_lunette),
       FOREIGN KEY(id_couleur) REFERENCES couleur(id_couleur),
       FOREIGN KEY(id_marque) REFERENCES marque(id_marque),
       FOREIGN KEY(id_fournisseur) REFERENCES fournisseur(id_fournisseur),
       FOREIGN KEY(id_categorie) REFERENCES categorie(id_categorie)
    )DEFAULT CHARSET utf8mb4;  
         '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE IF NOT EXISTS commande(
   id_commande INT,
   date_achat DATE,
   id_etat INT NOT NULL,
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_etat) REFERENCES Etat(id_etat),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
)DEFAULT CHARSET utf8mb4;
     '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE IF NOT EXISTS ligne_commande(
   id_lunette INT,
   id_commande INT,
   prix DECIMAL(12,2),
   quantite INT,
   PRIMARY KEY(id_lunette, id_commande),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette),
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
)DEFAULT CHARSET utf8mb4;
         '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE IF NOT EXISTS ligne_panier(
   id_lunette INT,
   id_utilisateur INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(id_lunette, id_utilisateur),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
    )DEFAULT CHARSET utf8mb4;
         '''
    mycursor.execute(sql)

    sql = ''' INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
    (1,'admin','admin@admin.fr',
        'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
        'ROLE_admin','admin','1'),
    (2,'client','client@client.fr',
        'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
        'ROLE_client','client','1'),
    (3,'client2','client2@client2.fr',
        'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
        'ROLE_client','client2','1');    '''
    mycursor.execute(sql)

    sql = ''' INSERT INTO couleur (id_couleur, libelle_couleur) VALUES
    (1, 'Noir'),
    (2, 'Blanc'),
    (3, 'Rouge'),
    (4, 'Bleu'),
    (5, 'Vert');'''
    mycursor.execute(sql)

    sql = ''' INSERT INTO categorie (id_categorie, libelle_categorie) VALUES
   (1, 'Lunettes de soleil'),
   (2, 'Lunettes de vue'),
   (3, 'Lunettes de sport'),
   (4, 'Lunettes pour enfant'),
   (5, 'Lunettes de mode');'''
    mycursor.execute(sql)

    sql = ''' INSERT INTO marque (id_marque, libelle_marque) VALUES
    (1, 'Ray-Ban'),
    (2, 'Oakley'),
    (3, 'Gucci'),
    (4, 'Prada'),
    (5, 'Dolce & Gabbana');'''
    mycursor.execute(sql)

    sql = '''INSERT INTO fournisseur (id_fournisseur, libelle_fournisseur) VALUES
    (1, 'Essilor'),
    (2, 'Luxottica'),
    (3, 'Marchon'),
    (4, 'Safilo');'''
    mycursor.execute(sql)

    sql = '''   INSERT INTO lunette (id_lunette, libelle_lunette, prix_lunette, id_couleur, id_categorie, id_marque, id_fournisseur) VALUES
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
    (16, 'Lunettes de mode jaunes', 300.00, 5, 5, 5, 4);'''
    mycursor.execute(sql)

    sql = ''' 
    INSERT INTO etat(id_etat, libelle_etat) VALUES (1,'en attente'),
                                                   (2,'expédié'),
                                                   (3,'validé'),
                                                   (4,'confirmé');
         '''
    mycursor.execute(sql)

    get_db().commit()
    return redirect('/')
