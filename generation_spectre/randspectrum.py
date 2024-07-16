# on part du principe qu'on va recevoir une liste composée des spectres des principaux gaz/métaux
# présents dans les étoiles, présentés sous la forme d'un dataset à 2 colonnes :
#         - wavelength : les longueurs d'ondes (bandes) principales de l'élément
#         - relint : l'intensité relative (luminosité) de chaque bande



###### PB ACTUEL :
# les index fonctionnent mal, si index pas présent
import pandas as pd
import numpy as np
import os
import random as rand
import matplotlib.pyplot as plt
from decimal import Decimal
from math import pow

min_elems_used = 4
max_elems_used = 5
min_relint_noise = 0
max_relint_noise = 50
min_wl_noise = 0
max_wl_noise = 1100
min_n_noise = 1500
max_n_noise = 2000

# recuperation de la liste des élélements fichier par fichier
def get_elements_list(path):
    filenames = os.listdir(path)
    dataframes = []
    for n in filenames:
        data = pd.read_csv(path + "\\" + n)
        # nomme le df en fonction de son element
        data.Name = n[:-4]
        dataframes.append(data) 
    return dataframes

# generation de spectres
def generate_spectrum(base_elements):
    """Retourne un spectre lumineux sous forme de dataframe et la liste de labels associés"""
    max_elems = len(base_elements)

    # ne peut pas être construit avec moins de 2 éléments // limite pas nécessaire ?
    if (max_elems < 2):
        print("not enough base elements provided")
        pass

    # création du df resultat en y ajoutant un nombre aléatoire d'éléments de base
    rand_elems = rand.choices(base_elements, k=rand.randrange(2, max_elems if max_elems < 5 else 5))
    labels = [x.Name for x in rand_elems]
    # df_res = pd.concat(rand.choices(base_elements, k=rand.randrange(1, max_elems)), ignore_index = True)
    df_res = pd.concat(rand_elems, ignore_index=True)

    # génère du bruit
    n_noise = rand.randint(min_n_noise, max_n_noise)
    rand_wls = [rand.uniform(min_wl_noise, max_wl_noise) for x in range(n_noise)] # créer en amont les valeurs de wl assure leur unicité // plus mtn mdr oups (reessayer avec sample)

    for n in range(0,n_noise):
        df_res.loc[len(df_res)] = {"wavelength": round(rand_wls[n], 1), "relint": round(rand.uniform(0, max_relint_noise), 1)} # max 1 nb après la virgule pour la wavelength et le relint

    # réordonne par wavelength
    df_res = df_res.sort_values("wavelength")

    return df_res, labels

def generate_spectrums(base_elements, n):
    """Retourne plusieurs spectre lumineux sous forme de dataframe et la matrice de labels associée"""
    max_elems = len(base_elements)
    list_df = []
    matrice_labels = pd.DataFrame(columns=[x.Name for x in base_elements])
    
    # ne peut pas être construit avec moins de 2 éléments // limite pas nécessaire ?
    if (max_elems < 2):
        print("not enough base elements provided")
        pass
    
    for i in range(n):
        # création du df resultat en y ajoutant un nombre aléatoire d'éléments de base
        rand_elems = rand.choices(base_elements, k=rand.randrange(2, max_elems if max_elems < 5 else 5))

        # initialisation du row
        matrice_labels.loc[i] = [0] * max_elems

        # changement du 0 en 1 pour noter les éléments présents
        for elem in rand_elems:
            matrice_labels.at[i, elem.Name] = 1

        # df_res = pd.concat(rand.choices(base_elements, k=rand.randrange(1, max_elems)), ignore_index = True)
        df_res = pd.concat(rand_elems, ignore_index=True)

        # génère du bruit
        n_noise = rand.randint(min_n_noise, max_n_noise)
        rand_wls = [rand.uniform(min_wl_noise, max_wl_noise) for x in range(n_noise)] # créer en amont les valeurs de wl assure leur unicité // plus mtn mdr oups (reessayer avec sample)

        for n in range(0,n_noise):
            df_res.loc[len(df_res)] = {"wavelength": round(rand_wls[n], 1), "relint": round(rand.uniform(0, max_relint_noise), 1)} # max 1 nb après la virgule pour la wavelength et le relint

        # réordonne par wavelength
        list_df.append(df_res.sort_values("wavelength"))

    return list_df, matrice_labels



def new_generate_spectrums(base_elements, n, step = 0.5):
    # ne peut pas être construit avec moins d' 1 element
    nb_elems = len(base_elements)

    if (nb_elems < min_elems_used):
        print("not enough base elements provided")
        pass

    # création du df labels
    labels = pd.DataFrame(data = np.zeros((n, nb_elems)), columns=[elem.Name for elem in base_elements])

    # génération des spectres
    list_df = []
    for i in range(n):
        # création du squelette + pré-remplissage avec du bruit
        array_wavelength = np.arange(0,max_wl_noise,step)
        array_relint = np.random.randint(min_relint_noise,max_relint_noise, array_wavelength.shape)
        df = pd.DataFrame(data ={"wavelength": array_wavelength , "relint": array_relint})
        # df.set_index("wavelength", inplace=True)

        # selection des éléments a rajouter
        rand_elems = rand.choices(base_elements, k=rand.randrange(min_elems_used, nb_elems if nb_elems < max_elems_used else max_elems_used))

        # loren ipsum
        for elem in rand_elems:
            # stockage des labels
            labels.at[i, elem.Name] = 1

            # loren ipsum
            # sorted_elem = elem.set_index("wavelength").reindex(array_wavelength)
            # sorted_elem = elem.sort_values('wavelength', ascending=True).drop_duplicates(["wavelength"], keep="last").set_index("wavelength").reindex(array_wavelength, method="nearest")
            elem["wavelength"] = elem["wavelength"].apply(lambda x: myround(x, step))

            # ajout au df
            df = pd.concat([df, elem], ignore_index=True)
            # indexes = next(idx for idx, row in sorted_elem.iterrows() if row["relint"] != np.nan)
            # values = next(row["relint"] for idx, row in sorted_elem.iterrows() if row["relint"] != np.nan)
        
        # traitement des doublons
        
        df = df.sort_values("relint", ascending=True).drop_duplicates(["wavelength"], keep="last").sort_values("wavelength", ascending=True).reset_index(drop=True)
        list_df.append(df)

    return list_df, labels


def myround(n, base):
    return base * round(n/base)

if __name__ == "__main__":
    path = "StellarAnalytics\generation_spectre\elements_presentation"

    elements = get_elements_list(path)
    spectrum, labels = generate_spectrums(elements, 1)
    print("matrice labels :", labels.iloc[0].to_string())
    print("spectre : ", spectrum[0])

    # plot pour voir la gueule que ça a avec les rectangles colonnes là
    plt.plot(spectrum[0]["wavelength"], spectrum[0]["relint"])
    plt.show()
