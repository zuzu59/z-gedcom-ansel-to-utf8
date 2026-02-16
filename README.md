# Petit script python pour convertir les fichiers GEDCOM ANSEL en charset UTF-8
zf260216.1755

En généalogie *informatique*, il y a toujours eu des problèmes pour la représentation des caractères accentués et très tôt, bien avant l'arrivée de l'Internet où on a eu le même problème mais au niveau mondial et qu'on a sorti la norme, l'UTF-8, ils ont *inventé* un format spécial pour gérer ces caractères accentués, le format ANSEL !

https://fr.wikipedia.org/wiki/GEDCOM

Les fichiers GEDCOM en format ANSEL, sont compatibles pour les logiciels de généalogie comme Heredis, Gramps, Webtree et autres, mais malheureusement pas pour le visualisateur Topola !

https://pewu.github.io/topola-viewer

J'ai donc fait un petit programme informatique qui les convertis en nouveau format UTF-8 !


# Utilisation
````
python3 gedcom_ansel_to_utf8.py [--inplace] [-o OUT] file1 [file2 ...]
````

# Validation du code GEDCOM
On peut utiliser Ged-Inline pour la vérification syntaxique de la qualité du fichier GEDCOM:

https://ged-inline.org/


