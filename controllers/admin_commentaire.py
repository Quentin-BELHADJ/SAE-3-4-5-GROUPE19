#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/article/commentaires', methods=['GET'])
def admin_article_details():
    mycursor = get_db().cursor()
    id_article =  request.args.get('id_article', None)
    sql = '''SELECT commentaire.*, utilisateur.nom
FROM commentaire 
LEFT JOIN utilisateur ON utilisateur.id_utilisateur = commentaire.id_utilisateur 
GROUP BY id_lunette, commentaire.id_utilisateur, date_publication, commentaire, valider, nom
ORDER BY valider, date_publication DESC;'''
    mycursor.execute(sql)
    commentaires = mycursor.fetchall()
    sql = '''   select * from lunette '''
    mycursor.execute(sql)
    article = mycursor.fetchall()
    return render_template('admin/article/show_article_commentaires.html'
                           , commentaires=commentaires
                           , article=article
                           )

@admin_commentaire.route('/admin/article/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_publication', None)
    tuple_delete = (id_utilisateur, id_article, date_publication)
    sql = ''' DELETE FROM commentaire WHERE id_utilisateur=%s AND id_lunette=%s AND date_publication=%s '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article='+id_article)


@admin_commentaire.route('/admin/article/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_article = request.args.get('id_article', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/article/add_commentaire.html',id_utilisateur=id_utilisateur,id_article=id_article,date_publication=date_publication )

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']   #1 admin
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    tuple_insert = (id_article, id_utilisateur ,date_publication,commentaire)
    sql = '''  INSERT INTO commentaire(id_lunette,id_utilisateur,date_publication,commentaire,valider) VALUES (%s,%s,%s,%s,1)'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article='+id_article)


@admin_commentaire.route('/admin/article/commentaires/valider', methods=['GET'])
def admin_comment_valider():
    mycursor = get_db().cursor()
    sql = '''UPDATE commentaire SET valider=1 WHERE valider IS NULL OR valider=0'''
    mycursor.execute(sql)
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article=')