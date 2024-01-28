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

    sql = '''SELECT id_lunette AS id_article, libelle_lunette as nom, prix_lunette AS prix FROM lunette ORDER BY libelle_lunette;'''
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

    articles_panier = []
    """
    sql = "SELECT * , 10 as prix , concat('nomarticle',lunette_id) as nom FROM ligne_panier"
    mycursor.execute(sql)
    articles_panier = mycursor.fetchall()"""

    if len(articles_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           #, prix_total=prix_total
                           , items_filtre=types_article
                           )
