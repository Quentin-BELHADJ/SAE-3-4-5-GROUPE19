#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')


@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = '''SELECT l.id_lunette AS id_article, nom_lunette as nom, prix_lunette AS prix , CONCAT(nom_lunette,'.jpg') AS image, SUM(d.stock) as stock, COALESCE(SUM(CASE WHEN d.stock = 0 THEN 1 ELSE 0 END), 0) AS empty_stock_count
    FROM lunette l
    LEFT JOIN declinaison d on l.id_lunette = d.id_lunette
    GROUP BY l.id_lunette, nom_lunette, prix_lunette
    ORDER BY nom_lunette;
    '''
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    return render_template('admin/article/show_article.html'
                           , articles=articles)



@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()

    return render_template('admin/article/add_article.html'
                           #,types_article=type_article,
                           #,couleurs=colors
                           #,tailles=tailles
                            )


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_article_id = request.form.get('type_article_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename=None

    sql = '''  requête admin_article_2 '''

    tuple_add = (nom, filename, prix, type_article_id, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'article ajouté , nom: ', nom, ' - type_article:', type_article_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'article ajouté , nom:' + nom + '- type_article:' + type_article_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = ''' requête admin_article_3 '''
    mycursor.execute(sql, id_article)
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet article : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' requête admin_article_4 '''
        mycursor.execute(sql, id_article)
        article = mycursor.fetchone()
        print(article)
        image = article['image']

        sql = ''' requête admin_article_5  '''
        mycursor.execute(sql, id_article)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un article supprimé, id :", id_article)
        message = u'un article supprimé, id : ' + id_article
        flash(message, 'alert-success')

    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET', 'POST'])
def edit_article():
    if request.method == 'GET':
        id_article = request.args.get('id_article')
        print(id_article)
        mycursor = get_db().cursor()
        sql = '''SELECT l.nom_lunette as nom, CONCAT(l.nom_lunette, '.jpg') as image, l.id_lunette as id_lunette, l.prix_lunette as prix, SUM(d.stock) AS stock 
        FROM lunette l 
        JOIN declinaison d on l.id_lunette = d.id_lunette 
        WHERE l.id_lunette =%s'''
        mycursor.execute(sql, (id_article,))
        article = mycursor.fetchone()
        print(article)

        sql = """SELECT COUNT(id_couleur) AS nbCouleur 
            FROM declinaison 
            WHERE id_lunette =%s;
            """

        mycursor.execute(sql, id_article)
        result = mycursor.fetchone()
        NbDeclinaisons = result['nbCouleur']
        print("NbDeclinaisons", NbDeclinaisons)

        sql = '''SELECT d.*, c.libelle AS couleur, l.nom_lunette
FROM declinaison d
JOIN couleur c ON d.id_couleur = c.id_couleur
JOIN lunette l ON d.id_lunette = l.id_lunette
WHERE d.id_lunette =%s'''

        mycursor.execute(sql, id_article)
        declinaison = mycursor.fetchall()
        print("Declinaison", declinaison)


        if article:
            return render_template('admin/article/edit_article.html'
                                   , article=article
                                   , nbCouleur=NbDeclinaisons
                                   , declinaison=declinaison)
        else:
            flash('L\'article sélectionné n\'existe pas', 'alert-danger')
            return redirect('/admin/article/show')
    elif request.method == 'POST':
        mycursor = get_db().cursor()
        id_article = request.form.get('id_article')
        new_stock = request.form.get('new_stock')
        id_couleur = request.form.get('id_couleur')
        print('id_article_start', id_article)
        print('new_stock_start', new_stock)
        print('id_couleur_starth', id_couleur)

        sql = '''SELECT COUNT(id_couleur) AS nbCouleur FROM declinaison 
                    WHERE id_lunette =%s;'''
        mycursor.execute(sql, (id_article,))

        result = mycursor.fetchone()
        NbDeclinaisons = result['nbCouleur']
        print("NbDeclinaisons", NbDeclinaisons)
        mycursor = get_db().cursor()

        if(NbDeclinaisons != 1):
            sql = '''UPDATE declinaison SET stock =%s WHERE id_lunette =%s AND id_couleur =%s'''
            mycursor.execute(sql, (new_stock, id_article, id_couleur))
            get_db().commit()
            print('id_article', id_article)
            print('id_couleur', id_couleur)
        else:
            sql = '''UPDATE declinaison SET stock =%s WHERE id_lunette =%s'''
            mycursor.execute(sql, (new_stock, id_article))
            get_db().commit()
            print('id_article', id_article)
            print('new_stock', new_stock)


        flash('Stock mis à jour avec succès', 'alert-success')
        return redirect('/admin/article/show')







@admin_article.route('/admin/article/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    article=[]
    commentaires = {}
    return render_template('admin/article/show_avis.html'
                           , article=article
                           , commentaires=commentaires
                           )


@admin_article.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    return admin_avis(article_id)
