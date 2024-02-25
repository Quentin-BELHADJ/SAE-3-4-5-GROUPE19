#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

from controllers.client_liste_envies import client_historique_add

client_commentaire = Blueprint('client_commentaire', __name__,
                        template_folder='templates')


@client_commentaire.route('/client/article/details', methods=['GET'])
def client_article_details():
    mycursor = get_db().cursor()
    id_article =  request.args.get('id_article', None)
    id_client = session['id_user']

    ## partie 4
    #client_historique_add(id_article, id_client)

    sql = '''SELECT l.prix_lunette AS prix, CONCAT(l.nom_lunette,'.jpg') AS image, SUM(d.stock)  AS stock, l.description AS description, l.nom_lunette AS nom FROM lunette l
    LEFT JOIN declinaison d ON d.id_lunette = l.id_lunette
    WHERE l.id_lunette = %s
    GROUP BY l.id_lunette
    '''
    mycursor.execute(sql, id_article)
    article = mycursor.fetchone()
    commandes_articles=[]
    nb_commentaires=[]
    if article is None:
        abort(404, "pb id article")
    sql = '''
    
    '''
    """
    mycursor.execute(sql, ( id_article))
    commentaires = mycursor.fetchall()
    """
    sql = '''SELECT IFNULL(SUM(lc.quantite),0) AS nb_commandes_article FROM ligne_commande lc
    LEFT JOIN commande c ON c.id_commande = lc.id_commande
    LEFT JOIN declinaison d ON d.id_declinaison = lc.id_declinaison
    WHERE c.id_utilisateur = %s AND d.id_lunette = %s;
    '''
    mycursor.execute(sql, (id_client, id_article))
    commandes_articles = mycursor.fetchone()
    """
    sql = '''
    '''
    
    mycursor.execute(sql, (id_client, id_article))
    note = mycursor.fetchone()
    print('note',note)
    if note:
    note=note['note']
    sql = '''
    '''
    mycursor.execute(sql, (id_client, id_article))"""
    nb_commentaires = mycursor.fetchone()
    return render_template('client/article_info/article_details.html'
                           , article=article
                           # , commentaires=commentaires
                           , commandes_articles=commandes_articles
                           # , note=note
                            , nb_commentaires=nb_commentaires
                           )

@client_commentaire.route('/client/commentaire/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    commentaire = request.form.get('commentaire', None)
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    if commentaire == '':
        flash(u'Commentaire non prise en compte')
        return redirect('/client/article/details?id_article='+id_article)
    if commentaire != None and len(commentaire)>0 and len(commentaire) <3 :
        flash(u'Commentaire avec plus de 2 caractères','alert-warning')              # 
        return redirect('/client/article/details?id_article='+id_article)

    tuple_insert = (commentaire, id_client, id_article)
    print(tuple_insert)
    sql = '''  '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)


@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''   '''
    tuple_delete=(id_client,id_article,date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/add', methods=['POST'])
def client_note_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_article = request.form.get('id_article', None)
    tuple_insert = (note, id_client, id_article)
    print(tuple_insert)
    sql = '''   '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/edit', methods=['POST'])
def client_note_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_article = request.form.get('id_article', None)
    tuple_update = (note, id_client, id_article)
    print(tuple_update)
    sql = '''  '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/delete', methods=['POST'])
def client_note_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    tuple_delete = (id_client, id_article)
    print(tuple_delete)
    sql = '''  '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)
