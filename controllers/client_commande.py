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
    sql = """SELECT lunette.nom_lunette AS nom, declinaison.prix AS prix, ligne_panier.quantite AS quantite FROM ligne_panier 
    LEFT JOIN declinaison ON declinaison.id_declinaison = ligne_panier.id_declinaison
    LEFT JOIN lunette ON declinaison.id_lunette = lunette.id_lunette
    WHERE ligne_panier.id_utilisateur = %s;"""
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
    sql = """SELECT lunette.nom_lunette AS nom, declinaison.prix AS prix, ligne_panier.quantite AS quantite FROM ligne_panier 
    LEFT JOIN declinaison ON declinaison.id_declinaison = ligne_panier.id_declinaison
    LEFT JOIN lunette ON declinaison.id_lunette = lunette.id_lunette
    WHERE ligne_panier.id_utilisateur = %s;"""
    mycursor.execute(sql, id_client)
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
         flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
         return redirect('/client/article/show')
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    a = datetime.strptime('my date', "%b %d %Y %H:%M")

    sql = ''' INSERT INTO commande (date_achat,id_etat,id_adresse,id_adresse_1, id_utilisateur) VALUES
            (%s,0,%s,%s,%s);'''
    mycursor.execute(sql,[a,adresse,adresse1,id_client])
    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute()
    num_last = mycursor.fetchone["last_insert_id"]
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
    sql = '''  selection des commandes ordonnées par état puis par date d'achat descendant '''
    commandes = []

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = ''' selection du détails d'une commande '''

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

