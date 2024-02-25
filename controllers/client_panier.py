#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_declinaison = request.form.get('id_article')
    id_utilisateur = session['id_user']
    quantite = int(request.form.get('quantite'))
    print("id_declinaison ", id_declinaison)
    print("id_utilisateur ",id_utilisateur)
    print("quantite ",quantite)

    try:
        mycursor.execute(f"SELECT stock FROM declinaison WHERE declinaison.id_lunette =%s;", (id_declinaison,))
        result = mycursor.fetchone()
        print("result ",result)

        if result:
            stock_actuel = result['stock']
            print("stock_actuel ",stock_actuel)

            # Vérifier si le stock est suffisant
            if stock_actuel >= quantite:
                # Mettre à jour le stock dans la table declinaison
                mycursor.execute(f"SELECT ligne_panier.id_utilisateur FROM ligne_panier WHERE id_utilisateur = {id_utilisateur} AND id_declinaison = {id_declinaison};")
                panier_utilisateur = mycursor.fetchone()
                if panier_utilisateur == None:
                    mycursor.execute(f"INSERT INTO ligne_panier (id_declinaison, id_utilisateur, quantite) SELECT l.id_lunette, {id_utilisateur}, {quantite} FROM lunette l WHERE l.id_lunette = {id_declinaison};")
                else :
                    mycursor.execute(f"UPDATE ligne_panier SET quantite = quantite + {quantite} WHERE id_utilisateur = {id_utilisateur} AND id_declinaison = {id_declinaison};")
                nouveau_stock = stock_actuel - quantite
                print('nouveau stock : ', nouveau_stock)
                mycursor.execute(
                    f"UPDATE declinaison SET stock = {nouveau_stock} WHERE declinaison.id_lunette = {id_declinaison}")
                get_db().commit()

                flash("L'article a été ajouté à votre panier avec succès.")
                return redirect('/client/article/show')
            else:
                flash("Stock insuffisant.")
                return redirect('/client/article/show')
        else:
            flash("La déclinaison spécifiée n'existe pas.")
            return redirect('/client/article/show')

    except Exception as e:
        flash(f"Une erreur s'est produite : {str(e)}")
        return redirect('/client/article/show')

    finally:
        mycursor.close()


@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_declinaison = request.form['id_declinaison']
    id_utilisateur = session['id_user']
    quantite = int(request.form.get('quantite'))
    print(id_declinaison)
    print(id_utilisateur)
    print(quantite)

    # Récupérer les détails de l'article dans le panier
    sql = '''SELECT l.id_declinaison as id_declinaison, l.id_utilisateur as id_utilisateur, l.quantite as quantite 
             FROM ligne_panier l WHERE l.id_utilisateur = %s AND l.id_declinaison = %s'''
    mycursor.execute(sql, (id_utilisateur, id_declinaison))
    article_panier = mycursor.fetchone()  # Utiliser fetchone() car on attend un seul résultat
    print(article_panier)
    print("something start")

    if article_panier:  # Vérifier si l'article est dans le panier
        if quantite > 1:
            print("something 1")
            # Diminuer la quantité de 1 dans le panier
            new_quantity = quantite - 1
            sql = '''UPDATE ligne_panier SET quantite = %s WHERE id_utilisateur = %s AND id_declinaison = %s'''
            mycursor.execute(sql, (new_quantity, id_utilisateur, id_declinaison))
            sql_update_stock = '''UPDATE declinaison SET stock = stock + 1 WHERE id_declinaison = %s'''
            mycursor.execute(sql_update_stock, (id_declinaison,))
        else:
            print("something 2")
            # Si la quantité est déjà à 1, supprimer l'article du panier
            sql = '''DELETE FROM ligne_panier WHERE id_utilisateur = %s AND id_declinaison = %s'''
            mycursor.execute(sql, (id_utilisateur, id_declinaison))
            sql_update_stock = '''UPDATE declinaison SET stock = stock + 1 WHERE id_declinaison = %s'''
            mycursor.execute(sql_update_stock, (id_declinaison,))

        print("something end")
        # Mise à jour du stock de l'article disponible
        get_db().commit()

    return redirect('/client/article/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']

    # Sélection des lignes de panier
    sql_select_panier = '''SELECT id_declinaison, quantite FROM ligne_panier WHERE id_utilisateur = %s'''
    mycursor.execute(sql_select_panier, (client_id,))
    items_panier = mycursor.fetchall()

    # Suppression de toutes les entrées correspondant à l'utilisateur connecté dans la table ligne_panier
    sql_delete_panier = '''DELETE FROM ligne_panier WHERE id_utilisateur = %s'''
    mycursor.execute(sql_delete_panier, (client_id,))

    # Mise à jour du stock pour chaque article supprimé
    for item in items_panier:
        id_declinaison = item['id_declinaison']
        quantite = item['quantite']

        sql_update_stock = '''UPDATE declinaison SET stock = stock + %s WHERE id_declinaison = %s'''
        mycursor.execute(sql_update_stock, (quantite, id_declinaison))

    get_db().commit()
    return redirect('/client/article/show')



@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')

    # Sélection de la ligne du panier à supprimer
    sql_select_panier = '''SELECT id_declinaison, quantite FROM ligne_panier WHERE id_utilisateur = %s AND id_declinaison = %s'''
    mycursor.execute(sql_select_panier, (id_client, id_article))
    panier_item = mycursor.fetchone()

    if panier_item:
        id_declinaison = panier_item['id_declinaison']
        quantite = panier_item['quantite']

        # Suppression de la ligne du panier
        sql_delete_panier = '''DELETE FROM ligne_panier WHERE id_utilisateur = %s AND id_declinaison = %s'''
        mycursor.execute(sql_delete_panier, (id_client, id_declinaison))

        # Mise à jour du stock de l'article
        sql_update_stock = '''UPDATE declinaison SET stock = stock + %s WHERE id_declinaison = %s'''
        mycursor.execute(sql_update_stock, (quantite, id_declinaison))

        get_db().commit()

    return redirect('/client/article/show')



@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    mycursor = get_db().cursor()

    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)

    session['filter_word'] = filter_word
    session['filter_prix_min'] = filter_prix_min
    session['filter_prix_max'] = filter_prix_max
    session['filter_types'] = filter_types

    sql = """
    SELECT l.id_lunette as id_lunette, l.nom_lunette as nom, l.prix_lunette as prix, CONCAT(l.nom_lunette, '.jpg') as image, d.stock as stock, l.id_marque as marque_id
    FROM lunette l 
    JOIN declinaison d on l.id_lunette = d.id_lunette
    """

    if filter_types:
        sql += " WHERE l.id_marque IN ({})".format(','.join(map(str, filter_types)))

    mycursor.execute(sql)
    articles = mycursor.fetchall()

    sql = '''SELECT id_marque AS id_type_article, libelle_marque AS libelle FROM marque ORDER BY libelle;'''
    mycursor.execute(sql)
    marques = mycursor.fetchall()


    if filter_word:
        articles = [article for article in articles if filter_word.lower() in article['nom'].lower()]
    if filter_prix_min:
        articles = [article for article in articles if article['prix'] >= float(filter_prix_min)]
    if filter_prix_max:
        articles = [article for article in articles if article['prix'] <= float(filter_prix_max)]



    # test des variables puis
    # mise en session des variables
    return render_template('/client/boutique/panier_article.html'
                           , articles=articles
                           , items_filtre=marques)


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    session['filter_word'] = None
    session['filter_prix_min'] = None
    session['filter_prix_max'] = None
    session['filter_types'] = None
    print("suppr filtre")
    return redirect('/client/article/show')
