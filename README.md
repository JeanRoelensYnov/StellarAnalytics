# StellarAnalytics

Ce projet a pour but de créer des spectres d'étoiles inventés de toute pièce. Il s'appuie sur les données de [NIST](https://www.nist.gov/pml/atomic-spectra-database-contents) pour contruire les spectres.


La structure est séparée en trois parties distinctes :

- La première est le scraping qui récupère les données des tables nécessaires. Pour chaque table, il récupère les longueurs d'onde ainsi que l'intensité relative correspondante.
- La deuxième partie est la création des spectres.
- La troisième est l'exploitation des spectres factices par nos modèles.

## Générer les données élèments

Pour cela, il vous suffit de lancer le script Python **"Generate_csv.py"**. Celui-ci va tourner pendant un certain temps pour récupérer toutes les données, donc ne soyez pas surpris si vous devez attendre.

Si vous pensez à un moment que le script ne génère rien, vous pouvez vérifier sous le chemin StellarAnalytics/Data/Output/ pour voir si le dossier a été créé et s'il se remplit progressivement.

Normalement, voici les éléments et les ionisations qui devraient être récupérés par le scraping :

| Composante chimique | Symbol | Ionization |
|-|-|-|
| Oxygen | O | I II III IV V VI VII
| Hydrogen | H | I
| Sodium | Na | I II III IV V VI VII VIII IX X XI
| Helium | He | I II
| Mercure | Hg | I II III
| Fer | Fe | I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI
| Magnésium | Mg | I II III IV V VI VII VIII IX X XI XII 
| Calcium | Ca | I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI
| Titane | Ti | I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX XXI XXII
| Nickel | Ni | I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX XXI XXII XXIII XXIV XXV XXVI XXVII XXVIII

Si certains éléments n'apparaissent pas à la fin de l'exécution du programme, il est simplement possible qu'aucune donnée ne soit disponible pour ces éléments.

## Générer les spectres

Ensuite, pour générer les spectres à partir des éléments scrapés, vous devez lancer le script **generate_data.py**. 

Vous pouvez spécifier le nombre de spectres à générer à la ligne **15** dans la fonction `new_generate_spectrums` en modifiant le deuxième paramètre (initialement mis à 1000).

## Lancer les modèles

Pour cela, vous avez à votre disposition deux fichiers qui se chargent de lancer la génération des spectres ainsi que l'essai du modèle sur les données générées.

Le premier fichier, nommé **"model.py"**, est normalement moins performant que le second, mais il traite les labels (éléments chimiques composant le spectre) en bloc.

Après avoir entraîné le modèle, vous devriez obtenir une approximation de sa précision dans le terminal.

Pour le second modèle, **model_forest.py**, il divise la charge de travail : plutôt que de traiter tous les labels en un seul bloc, il les traite en plus petits morceaux.

Tout comme le premier, après avoir entraîné le modèle, vous devriez obtenir une approximation de sa précision.

## Contact

Si jamais vous remarquez des oublis, des manquements, des optimisations, ou encore des bugs, vous êtes libre de nous contacter aux adresses suivantes :

Jean Roelens : jean.roelens@ynov.com

Axelle Refeyton : axelle.refeyton@ynov.com