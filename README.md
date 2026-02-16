# Petit script python pour convertir les fichiers GEDCOM ANSEL en charset UTF-8
zf260216.2251

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


# Détection de problèmes d'encodage UTF-8
On peut avoir deux façon d'encoder les caractères accentués en UTF-8

## La forme « Composée » (NFC) 
La version la plus courante (souvent sous Windows ou sur le Web) utilise un seul caractère unique pour le « é ».

Stéphanie : S + t + é (U+00E9) + p + h + a + n + i + e

Nombre de caractères : 9. 

## La forme « Décomposée » (NFD) 
Certains systèmes (comme macOS pour ses noms de fichiers) décomposent l'accent en deux éléments : une lettre de base et un accent « flottant ». 

Stéphanie : S + t + e (U+0065) + ́ (accent aigu U+0301) + p + h + a + n + i + e.

Nombre de caractères : 10. 

Pour les différencier, on peut utiliser l'utilitaire uniname (apt update ; apt install uniutils) avec l'exemple du problème avec le fichier Stéphanie.txt :

````
uniname Stéphanie.txt
````

ou directement avec un string :

````
echo -e "Stéphanie" |uniname
````
