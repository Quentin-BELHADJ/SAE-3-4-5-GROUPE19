from flask import Blueprint, request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_article = Blueprint('admin_declinaison_article', __name__, template_folder='templates')


@admin_declinaison_article.route('/admin/declinaison_article/add')
def add_declinaison_article():
    id_article = request.args.get('id_article')
    mycursor = get_db().cursor()
    article = None  # Récupérer l'article correspondant à id_article depuis la base de données
    couleurs = None  # Récupérer les couleurs disponibles depuis la base de données
    sexes = None  # Récupérer les sexes disponibles depuis la base de données
    return render_template('admin/article/add_declinaison_article.html', article=article, couleurs=couleurs, sexes=sexes)


@admin_declinaison_article.route('/admin/declinaison_article/add', methods=['POST'])
def valid_add_declinaison_article():
    mycursor = get_db().cursor()

    id_article = request.form.get('id_article')
    stock = request.form.get('stock')
    couleur = request.form.get('couleur')
    sexe = request.form.get('sexe')

    # Enregistrer la nouvelle déclinaison dans la base de données
    # Attention aux doublons

    get_db().commit()
    return redirect('/admin/article/edit?id_article=' + id_article)


@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['GET'])
def edit_declinaison_article():
    id_declinaison_article = request.args.get('id_declinaison_article')
    mycursor = get_db().cursor()
    declinaison_article = None  # Récupérer la déclinaison correspondante à id_declinaison_article depuis la base de données
    couleurs = None  # Récupérer les couleurs disponibles depuis la base de données
    sexes = None  # Récupérer les sexes disponibles depuis la base de données
    return render_template('admin/article/edit_declinaison_article.html', declinaison_article=declinaison_article, couleurs=couleurs, sexes=sexes)


@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['POST'])
def valid_edit_declinaison_article():
    id_declinaison_article = request.form.get('id_declinaison_article')
    id_article = request.form.get('id_article')
    stock = request.form.get('stock')
    couleur = request.form.get('couleur')
    sexe = request.form.get('sexe')

    # Mettre à jour la déclinaison dans la base de données avec les nouvelles valeurs

    message = u'Déclinaison modifiée, id : ' + str(id_declinaison_article) + ', Stock : ' + str(stock) + ', Couleur : ' + couleur + ', Sexe : ' + sexe
    flash(message, 'alert-success')
    return redirect('/admin/article/edit?id_article=' + id_article)


@admin_declinaison_article.route('/admin/declinaison_article/delete', methods=['GET'])
def admin_delete_declinaison_article():
    id_declinaison_article = request.args.get('id_declinaison_article')
    id_article = request.args.get('id_article')

    # Supprimer la déclinaison de la base de données

    flash(u'Déclinaison supprimée, id : ' + str(id_declinaison_article), 'alert-success')
    return redirect('/admin/article/edit?id_article=' + str(id_article))
