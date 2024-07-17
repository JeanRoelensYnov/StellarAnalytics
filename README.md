# StellarAnalytics

Ce projet à pour but de créer des spectres d'étoiles inventer de toute pièce. Il s'appuie sur les données de [NIST](https://www.nist.gov/pml/atomic-spectra-database-contents) pour pouvoir contruire les spectres.

La structure est séparé en deux partie distincte : 
- La premiére est le scrapper qui va venir récupérer les données des tables nécessaires, pour chacune des tables il récupére les longueur d'ondes ainsi que la intensité relative correspondante.
- La deuxiéme partie est l'exploitation de ces donnèes et la création des spectres, ainsi qu'un test d'un modèle de multi labelling (XGBoost) pour voir la précision de notre jeux de donnèes généré.

## Générer les données élèments

Pour ça il vous suffit de lancer le script python **"Generate_csv.py"** celui-ci va se lancer pendant un long moment pour pouvoir récupérer toute les données donc ne soyez pas surpris si vous devez attendre.

Si vous soupçonnez un moment le script ne génére rien vous pouvez vérifier sous le chemin StellarAnalytics/Data/Output/ si déjà pour commencer le dossier est crée et également si celui ce remplis petit à petit. 

Normalement voici les éléments et ionization qui devrait être récupéré par le scrapper : 

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

Si certains n'apparaissent pas lors de la fin de l'éxécution du programme il est tout simplement possible que aucune donnée ne soit disponible.

## Lancer les modèles

Pour cela vous avez à votre disposition deux fichiers qui s'occuperont de lancer la génération de spectre ainsi que l'essai du modèle sur les données généré.

Le premier du nom de **"model.py"** est normalement moins performant que le second mais celui-ci va traiter les labels (éléments chimique composant le spectre) d'un bloc. 
Pour choisir le nombre de spectre sur lequel le modèle devrait travailler aller à la ligne **16** et dans la fonction generate_spectrums renseigner le nombre désiré. 

Après avoir finis de générer et d'entrainer le modèle dessus vous devriez avoir une approximation de sa précision dans le terminal.

Pour le second modèle **model_forest.py** il s'agit enfaite d'une division de la charge de travail, plutôt que de traiter tout les labels en un seul bloc on en fait de plus petit morceaux. Tout comme **model.py** si vous souhaitez changer le nombre de spectre sur lequel celui-ci doit travailler modifier le second paramètre de la fonction generate_spectrums ligne **18**.

Tout comme le premier après avoir finis de générer et d'entrainer le modèle dessus vous devriez avoir une approximation de sa précision.

## Contact

Si jamais vous remarquez des oublis, manquement ou encore des optimisations ou bug vous êtes libre de nous contacter aux adresses suivante : 

Jean Roelens : jean.roelens@ynov.com

Axelle Refeyton : axelle.refeyton@ynov.com