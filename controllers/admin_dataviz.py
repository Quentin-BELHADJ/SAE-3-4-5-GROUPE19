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
    mycursor.execute("""
            SELECT m.libelle_marque AS marque, SUM(d.prix) AS somme_prix
            FROM lunette l
            INNER JOIN marque m ON l.id_marque = m.id_marque
            INNER JOIN declinaison d ON l.id_lunette = d.id_lunette
            GROUP BY m.libelle_marque;
        """)
    result = mycursor.fetchall()

    marques = [row['marque'] for row in result]
    sommes_prix = [row['somme_prix'] for row in result]
    print('marques', marques)
    print('sommes_prix', sommes_prix)
    zipped_data = zip(marques, sommes_prix)

    mycursor.execute("""
                SELECT m.libelle_marque AS marque, COUNT(d.id_declinaison) AS nb_declinaisons
                FROM lunette l
                INNER JOIN marque m ON l.id_marque = m.id_marque
                INNER JOIN declinaison d ON l.id_lunette = d.id_lunette
                GROUP BY m.libelle_marque;
            """)
    result_decli = mycursor.fetchall()

    marques_decli = [row['marque'] for row in result_decli]
    nb_declinaisons = [row['nb_declinaisons'] for row in result_decli]
    zipped_declinaisons = zip(marques, nb_declinaisons)

    return render_template('admin/dataviz/dataviz_etat_1.html', marques=marques, sommes_prix=sommes_prix, zipped_data=zipped_data, marques_decli=marques_decli,  nb_declinaisons=nb_declinaisons, zipped_declinaisons=zipped_declinaisons)


@admin_dataviz.route('/admin/dataviz/commentaires')
def show_data_comm():
    mycursor = get_db().cursor()
    sql = '''SELECT COUNT(id_lunette) as nb_commentaire FROM commentaire;'''
    mycursor.execute(sql)
    nb_commentaire = mycursor.fetchone()

    print(nb_commentaire)

    mycursor = get_db().cursor()
    sql = '''SELECT
    cl.libelle_categorie AS categorie, cl.id_categorie_lunette as id_categorie,
    COUNT(c.id_lunette) AS nombre_commentaires
FROM
    categorie_lunette cl
LEFT JOIN
    lunette l ON l.id_categorie_lunette = cl.id_categorie_lunette
LEFT JOIN
    commentaire c ON c.id_lunette = l.id_lunette
GROUP BY
    cl.libelle_categorie,cl.id_categorie_lunette;'''
    mycursor.execute(sql)
    categorie_lunette = mycursor.fetchall()

    print(categorie_lunette)
    mycursor = get_db().cursor()
    sql = '''SELECT
    l.nom_lunette AS libelle,
    IFNULL(AVG(n.note), 0) AS moyenne_note
FROM
    lunette l
LEFT JOIN
    note n ON n.id_lunette = l.id_lunette
GROUP BY
    l.nom_lunette;'''
    mycursor.execute(sql)
    datas_show = mycursor.fetchall()
    labels = [str(row['libelle']) for row in datas_show]
    values = [float(row['moyenne_note']) for row in datas_show]




    return render_template('admin/dataviz/dataviz_commentaires.html',
                            nb_commentaire = nb_commentaire,
                           categorie_lunette=categorie_lunette
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


