#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_liste_envies = Blueprint('client_liste_envies', __name__,
                        template_folder='templates')


@client_liste_envies.route('/client/envie/add', methods=['get'])
def client_liste_envies_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.args.get('id_article')
    
    sql = """SELECT * FROM liste_envie WHERE id_utilisateur = %s AND id_lunette = %s"""
    mycursor.execute(sql, (id_client, id_article))
    if mycursor.fetchone():
        sql = "DELETE FROM liste_envie WHERE id_lunette = %s AND id_utilisateur = %s"
        flash(u'Lunette supprimé de la wishlist', 'alert-warning') 
    else:
        sql = """INSERT INTO liste_envie VALUES (%s,%s,NOW());"""
        flash(u'Lunette ajouté à la wishlist', 'alert-success') 
        
    
    mycursor.execute(sql, (id_article,id_client))
    get_db().commit()

    return redirect('/client/article/show')

@client_liste_envies.route('/client/envie/delete', methods=['get'])
def client_liste_envies_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.args.get('id_article')
    sql = "DELETE FROM liste_envie WHERE id_utilisateur = %s AND id_lunette = %s"
    mycursor.execute(sql, (id_client, id_article))
    get_db().commit()
    return redirect('/client/envies/show')

@client_liste_envies.route('/client/envies/show', methods=['get'])
def client_liste_envies_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = """SELECT l.nom_lunette AS nom, l.id_lunette AS id_article, l.prix_lunette AS prix,  CONCAT(l.nom_lunette,'.jpg')  AS image FROM liste_envie le
        JOIN lunette l ON l.id_lunette = le.id_lunette
        WHERE le.id_utilisateur = %s
        ORDER BY le.date_update DESC"""
    mycursor.execute(sql, (id_client))
    articles_liste_envies = mycursor.fetchall()
    sql = "DELETE FROM historique WHERE id_utilisateur=%s AND MONTH(NOW()- date_consultation) >= 1;"
    mycursor.execute(sql, id_client);
    get_db().commit()
    mycursor = get_db().cursor()
    sql = """SELECT prix_lunette AS prix,  CONCAT(nom_lunette,'.jpg') AS image, nom_lunette AS lunette 
    FROM historique  JOIN lunette ON historique.id_lunette = lunette.id_lunette WHERE id_utilisateur = %s ORDER BY date_consultation DESC"""
    mycursor.execute(sql, id_client)
    articles_historique = mycursor.fetchall()
    return render_template('client/liste_envies/liste_envies_show.html'
                           ,articles_liste_envies=articles_liste_envies
                           , articles_historique=articles_historique
                           , nb_liste_envies= len(articles_liste_envies)
                           )



def client_historique_add(article_id, client_id):
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql ='''DELETE FROM historique WHERE id_utilisateur=%s and id_lunette=%s'''
    mycursor.execute(sql, (client_id,article_id))
    sql = 'INSERT INTO historique VALUES (%s,%s, NOW())'
    mycursor.execute(sql, (article_id, client_id))
    sql ='''SELECT * FROM historique WHERE id_utilisateur=%s'''
    mycursor.execute(sql, (client_id))
    historique_produit = mycursor.fetchall()
    if len(historique_produit) > 6:
        sql = '''DELETE FROM historique WHERE date_consultation = (SELECT MIN(date_consultation) FROM historique) AND id_utilisateur=%s;'''
        mycursor.execute(sql, client_id)
    get_db().commit()


@client_liste_envies.route('/client/envies/up', methods=['get'])
@client_liste_envies.route('/client/envies/down', methods=['get'])
@client_liste_envies.route('/client/envies/last', methods=['get'])
@client_liste_envies.route('/client/envies/first', methods=['get'])
def client_liste_envies_article_move():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.args.get('id_article')

    
    if "first" in str(request.url):
        sql = "UPDATE liste_envie SET date_update = NOW() WHERE id_lunette=%s AND id_utilisateur=%s"
        mycursor.execute(sql,(id_article, id_client))
        
    elif "last" in str(request.url):
         sql = "SELECT date_update FROM liste_envie WHERE id_utilisateur=%s ORDER BY date_update"
         mycursor.execute(sql,id_client)
         date = mycursor.fetchone()["date_update"]
         sql = "UPDATE liste_envie SET date_update = DATE_SUB(%s, INTERVAL 1 SECOND) WHERE id_lunette=%s AND id_utilisateur=%s "
         mycursor.execute(sql,(date,id_article, id_client))
    elif "down" in str(request.url):
        sql = "SELECT date_update FROM liste_envie WHERE id_utilisateur=%s AND id_lunette=%s"
        mycursor.execute(sql,(id_client, id_article))
        date = mycursor.fetchone()["date_update"]
        sql = "SELECT id_lunette, date_update FROM liste_envie WHERE date_update < %s AND id_utilisateur=%s ORDER BY date_update DESC"
        mycursor.execute(sql, (date, id_client))
        result = mycursor.fetchone()
        id_article2 = result["id_lunette"]
        date2 = result["date_update"]  
        sql = "UPDATE liste_envie SET date_update = %s WHERE id_lunette=%s AND id_utilisateur=%s"
        mycursor.execute(sql,(date,id_article2, id_client))
        mycursor.execute(sql,(date2,id_article, id_client))
    else:
        sql = "SELECT date_update FROM liste_envie WHERE id_utilisateur=%s AND id_lunette=%s"
        mycursor.execute(sql,(id_client, id_article))
        date = mycursor.fetchone()["date_update"]
        sql = "SELECT id_lunette, date_update FROM liste_envie WHERE date_update > %s AND id_utilisateur=%s ORDER BY date_update ASC"
        mycursor.execute(sql, (date, id_client))
        result = mycursor.fetchone()
        id_article2 = result["id_lunette"]
        date2 = result["date_update"]  
        sql = "UPDATE liste_envie SET date_update = %s WHERE id_lunette=%s AND id_utilisateur=%s"
        mycursor.execute(sql,(date,id_article2, id_client))
        mycursor.execute(sql,(date2,id_article, id_client))
        
         
        
    get_db().commit()
    return redirect('/client/envies/show')
