SELECT l.id_lunette AS id_article, l.nom_lunette as nom, l.prix_lunette AS prix , CONCAT(l.nom_lunette,'.jpg') AS image,
IF(EXISTS(SELECT * FROM liste_envie le WHERE le.id_lunette = l.id_lunette AND le.id_utilisateur = %s),1,0) AS liste_envie
FROM lunette l 
ORDER BY nom_lunette