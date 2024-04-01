#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = """SELECT 
    lunette.nom_lunette AS nom, 
    declinaison.prix AS prix, 
    ligne_panier.quantite AS quantite,
    couleur.libelle AS libelle_couleur
FROM 
    ligne_panier 
LEFT JOIN 
    declinaison ON declinaison.id_declinaison = ligne_panier.id_declinaison
LEFT JOIN 
    lunette ON declinaison.id_lunette = lunette.id_lunette
LEFT JOIN
    couleur ON declinaison.id_couleur = couleur.id_couleur
WHERE 
    ligne_panier.id_utilisateur = %s;
"""
    mycursor.execute(sql, id_client)
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    sql = "SELECT * FROM adresse WHERE id_utilisateur = %s"
    mycursor.execute(sql,id_client)
    adresses = mycursor.fetchall()
    return render_template('client/boutique/panier_validation_adresses.html'
                           , adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    adresse = request.form.get("id_adresse_livraison")
    adresse1 = request.form.get("id_adresse_facturation")
    
    id_client = session['id_user']
    sql = """SELECT * FROM ligne_panier 
    LEFT JOIN declinaison ON declinaison.id_declinaison = ligne_panier.id_declinaison
    LEFT JOIN lunette ON declinaison.id_lunette = lunette.id_lunette
    WHERE ligne_panier.id_utilisateur = %s;"""
    mycursor.execute(sql, id_client)
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
         flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
         return redirect('/client/article/show')
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    a = datetime.strptime("jan 11 2018 09:15", "%b %d %Y %H:%M")

    sql = ''' INSERT INTO commande (date_achat,id_etat,id_adresse,id_adresse_1, id_utilisateur) VALUES
            (%s,1,%s,%s,%s);'''
    mycursor.execute(sql,[a,adresse,adresse1,id_client])
    sql = '''SELECT last_insert_id() as last_insert_id'''
    #sql = """SELECT MAX(id_commande) AS last_insert_id FROM commande;"""
    mycursor.execute(sql)
    num_last = mycursor.fetchone()["last_insert_id"]
    for item in items_ligne_panier:
        sql = '''DELETE FROM ligne_panier WHERE id_declinaison = %s AND id_utilisateur = %s'''
        mycursor.execute(sql, [item["id_declinaison"],id_client])
        sql = "INSERT INTO ligne_commande VALUES (%s,%s,%s,%s);"
        mycursor.execute(sql, [item["id_declinaison"],num_last,item["quantite"],item["prix"]])

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = """ SELECT SUM(lc.quantite) AS nbr_articles,  c.date_achat AS date_achat, SUM(d.prix*lc.quantite) AS prix_total, e.libelle_etat AS libelle, c.id_commande AS id_commande, c.id_etat AS etat_id FROM commande c
            LEFT JOIN ligne_commande lc ON lc.id_commande = c.id_commande
            LEFT JOIN declinaison d ON d.id_declinaison = lc.id_declinaison
            LEFT JOIN etat e ON e.id_etat = c.id_etat
            WHERE c.id_utilisateur = %s
            GROUP BY c.id_commande
            ORDER BY c.id_etat, c.date_achat DESC;"""
    mycursor.execute(sql,id_client)     
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        sql = '''SELECT a.nom AS nom_livraison, a.rue AS rue_livraison,a.code_postal AS code_postal_livraison, a.ville AS ville_livraison,
                a1.nom AS nom_facturation, a1.rue AS rue_facturation, a1.code_postal AS code_postal_facturation, a1.ville AS ville_facturation
                FROM commande c
                LEFT JOIN adresse a ON c.id_adresse = a.id_adresse
                LEFT JOIN adresse a1 ON c.id_adresse_1 = a1.id_adresse
                WHERE c.id_commande = %s'''
        mycursor.execute(sql,id_commande)
        commande_adresses = mycursor.fetchone()
        sql = """SELECT 
    l.nom_lunette AS nom, 
    d.prix AS prix, 
    lc.quantite AS quantite, 
    lc.quantite * d.prix AS prix_ligne,
    couleur.libelle AS libelle_couleur
FROM 
    commande c
LEFT JOIN 
    utilisateur u ON c.id_utilisateur = u.id_utilisateur
LEFT JOIN 
    ligne_commande lc ON lc.id_commande = c.id_commande
LEFT JOIN 
    declinaison d ON d.id_declinaison = lc.id_declinaison
LEFT JOIN 
    lunette l ON d.id_lunette = l.id_lunette
LEFT JOIN 
    couleur ON d.id_couleur = couleur.id_couleur
WHERE  
    c.id_commande = %s;
"""
        mycursor.execute(sql,id_commande)
        articles_commande = mycursor.fetchall()

        print(articles_commande)
        print(commandes)
        print(articles_commande)

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

