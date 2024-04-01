#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session
from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql =  '''
    SELECT
    l.id_lunette AS id_article,
    l.nom_lunette AS nom,
    l.prix_lunette AS prix,
    CONCAT(nom_lunette, '.jpg') AS image,
    (SELECT SUM(stock) FROM declinaison WHERE id_lunette = l.id_lunette) AS stock,
    COUNT(d.id_couleur) AS nb_declinaisons,
    COUNT(DISTINCT c.date_publication) AS nb_avis,
    COUNT(DISTINCT n.id_utilisateur) AS nb_notes,
    IFNULL(AVG(n.note), 0) AS moy_notes,
    GROUP_CONCAT(d.id_declinaison) AS id_declinaison
FROM
    lunette l
JOIN
    declinaison d ON l.id_lunette = d.id_lunette
LEFT JOIN
    commentaire c ON l.id_lunette = c.id_lunette
LEFT JOIN
    note n ON l.id_lunette = n.id_lunette
GROUP BY
    l.id_lunette, l.nom_lunette, l.prix_lunette, CONCAT(nom_lunette, '.jpg')
ORDER BY
    nom_lunette;
    '''

    mycursor.execute(sql)
    lunettes = mycursor.fetchall()

    sql = '''SELECT id_marque AS id_type_article, libelle_marque AS libelle FROM marque ORDER BY libelle;'''
    mycursor.execute(sql)
    marques = mycursor.fetchall()
    
    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3=''' prise en compte des commentaires et des notes dans le SQL    '''
    articles = lunettes


    # pour le filtre
    types_article = marques
    sql = """SELECT 
    lunette.id_lunette AS id_article,
    lunette.nom_lunette AS nom,
    lunette.prix_lunette AS prix,
    ligne_panier.quantite AS quantite,
    ligne_panier.id_declinaison AS id_declinaison,
    couleur.libelle AS libelle_couleur
FROM 
    ligne_panier
JOIN 
    declinaison ON declinaison.id_declinaison = ligne_panier.id_declinaison
JOIN 
    lunette ON declinaison.id_lunette = lunette.id_lunette
LEFT JOIN 
    couleur ON declinaison.id_couleur = couleur.id_couleur
WHERE 
    ligne_panier.id_utilisateur = %s;
"""
    mycursor.execute(sql, (id_client,))
    articles_panier = mycursor.fetchall()
    print('articles_panier', articles_panier)

    if len(articles_panier) >= 1:
        sql = ''' SELECT SUM(d.prix*lp.quantite) AS prix FROM ligne_panier lp
                   LEFT JOIN declinaison d ON d.id_declinaison = lp.id_declinaison WHERE lp.id_utilisateur = %s'''
        mycursor.execute(sql,id_client)
        prix_total = mycursor.fetchone()["prix"]
    else:
        prix_total = None

    #print(articles)
    #print(articles_panier)
    #print(prix_total)
    #print(types_article)

    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , items_filtre=types_article
                           )
