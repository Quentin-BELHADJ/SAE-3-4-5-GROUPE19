#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = '''SELECT SUM(lc.quantite) AS nbr_articles, u.login AS login, c.date_achat AS date_achat, SUM(d.prix*lc.quantite) AS prix_total, e.libelle_etat AS libelle, c.id_commande AS id_commande, c.id_etat AS etat_id FROM commande c
            LEFT JOIN utilisateur u ON c.id_utilisateur = u.id_utilisateur
            LEFT JOIN ligne_commande lc ON lc.id_commande = c.id_commande
            LEFT JOIN declinaison d ON d.id_declinaison = lc.id_declinaison
            LEFT JOIN etat e ON e.id_etat = c.id_etat
            GROUP BY c.id_commande;'''
            
    mycursor.execute(sql)
    commandes=mycursor.fetchall()

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
        sql = """SELECT l.nom_lunette AS nom, d.prix AS prix, lc.quantite AS quantite, lc.quantite*d.prix AS prix_ligne FROM commande c
                LEFT JOIN utilisateur u ON c.id_utilisateur = u.id_utilisateur
                LEFT JOIN ligne_commande lc ON lc.id_commande = c.id_commande
                LEFT JOIN declinaison d ON d.id_declinaison = lc.id_declinaison
                LEFT JOIN lunette l ON d.id_lunette = l.id_lunette
                WHERE  c.id_commande = %s"""
        mycursor.execute(sql,id_commande)
        articles_commande = mycursor.fetchall()
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        sql = '''UPDATE commande SET id_etat = 2 WHERE id_commande = %s;'''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')
