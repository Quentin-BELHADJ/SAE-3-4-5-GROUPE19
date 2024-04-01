#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                        template_folder='templates')

@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_article_stock():
    mycursor = get_db().cursor()
    sql = '''
    
           '''
    # mycursor.execute(sql)
    # datas_show = mycursor.fetchall()
    # labels = [str(row['libelle']) for row in datas_show]
    # values = [int(row['nbr_articles']) for row in datas_show]

    # sql = '''
    #         
    #        '''
    datas_show=[]
    labels=[]
    values=[]

    return render_template('admin/dataviz/dataviz_etat_1.html'
                           , datas_show=datas_show
                           , labels=labels
                           , values=values)


@admin_dataviz.route('/admin/dataviz/commentaires')
def show_data_comm():
    mycursor = get_db().cursor()
    sql = '''SELECT
    c.id_categorie,
    cat.libelle AS categorie,
    COUNT(c.id_commentaire) AS nombre_commentaires,
    IFNULL(AVG(n.note), 0) AS note_moyenne
FROM
    commentaire c
LEFT JOIN
    note n ON c.id_commentaire = n.id_commentaire
JOIN
    article a ON c.id_article = a.id_article
JOIN
    categorie cat ON a.id_categorie = cat.id_categorie
GROUP BY
    c.id_categorie, cat.libell
           '''
    # mycursor.execute(sql)
    # datas_show = mycursor.fetchall()
    # labels = [str(row['libelle']) for row in datas_show]
    # values = [int(row['nbr_articles']) for row in datas_show]

    # sql = '''
    #
    #        '''
    datas_show = []
    labels = []
    values = []

    return render_template('admin/dataviz/dataviz_commentaires.html'
                           , datas_show=datas_show
                           , labels=labels
                           , values=values)


@admin_dataviz.route('/admin/dataviz/etat_wish_list')
def show_liste_envie_data():
    mycursor = get_db().cursor()
    sql = '''
            SELECT nom_lunette, nb_consultation FROM lunette;
           '''
    mycursor.execute(sql)
    datas_show = mycursor.fetchall()
    labels = [str(row['nom_lunette']) for row in datas_show]
    values = [int(row['nb_consultation']) for row in datas_show]
    sql = '''
             SELECT cl.libelle_categorie AS libelle, (SELECT COUNT(*) FROM liste_envie le JOIN lunette l ON le.id_lunette = l.id_lunette WHERE l.id_categorie_lunette = cl.id_categorie_lunette) AS nombre_envies
                FROM categorie_lunette cl
            '''
    mycursor.execute(sql)
    datas_show = mycursor.fetchall()

    return render_template('admin/dataviz/dataviz_etat_wishlist.html'
                           , datas_show=datas_show
                           , labels=labels
                           , values=values)

# sujet 3 : adresses


@admin_dataviz.route('/admin/dataviz/etat2')
def show_dataviz_map():
    # mycursor = get_db().cursor()
    # sql = '''    '''
    # mycursor.execute(sql)
    # adresses = mycursor.fetchall()

    #exemples de tableau "résultat" de la requête
    adresses =  [{'dep': '25', 'nombre': 1}, {'dep': '83', 'nombre': 1}, {'dep': '90', 'nombre': 3}]

    # recherche de la valeur maxi "nombre" dans les départements
    # maxAddress = 0
    # for element in adresses:
    #     if element['nbr_dept'] > maxAddress:
    #         maxAddress = element['nbr_dept']
    # calcul d'un coefficient de 0 à 1 pour chaque département
    # if maxAddress != 0:
    #     for element in adresses:
    #         indice = element['nbr_dept'] / maxAddress
    #         element['indice'] = round(indice,2)

    print(adresses)

    return render_template('admin/dataviz/dataviz_etat_map.html'
                           , adresses=adresses
                          )


