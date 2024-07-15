# on part du principe qu'on va recevoir une liste composée des spectres des principaux gaz/métaux
# présents dans les étoiles, présentés sous la forme d'un dataset à 3 entrées :
#         -  wavelength : les longueurs d'ondes (bandes) principales de l'élément
#         - relint : l'intensité relative (luminosité) de chaque bande
#         - chemical : la ou les 

import pandas as pd
import numpy as np
import os
import random as rand
import matplotlib.pyplot as plt

max_relint_noise = 50
min_wl_noise = 0
max_wl_noise = 1100
min_n_noise = 1500
max_n_noise = 2000

# recuperation de la liste des élélements
def get_elements_list(path):
    filenames = os.listdir(path)
    dataframes = []
    for n in filenames:
        data = pd.read_csv(path + "\\" + n)
        # nomme le df en fonction de son element
        data.Name = n[:-4]
        dataframes.append(data) # version sans le label "chemical"
        # data = pd.read_csv(path + "\\" + n)
        # ajout du label "Chemical"
        # data["Chemical"] = [n[:-4]] * len(data)
        # print(data.info)
        # dataframes.append(data)
    
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
    """Retourne plusieurs spectre lumineux sous forme de dataframe et la liste des labels associés"""
    max_elems = len(base_elements)
    list_df = []
    list_labels = []
    
    # ne peut pas être construit avec moins de 2 éléments // limite pas nécessaire ?
    if (max_elems < 2):
        print("not enough base elements provided")
        pass
    
    for i in range(n):
        # création du df resultat en y ajoutant un nombre aléatoire d'éléments de base
        rand_elems = rand.choices(base_elements, k=rand.randrange(2, max_elems if max_elems < 5 else 5))
        print(rand_elems)
        list_labels.append([x.Name for x in rand_elems])

        # df_res = pd.concat(rand.choices(base_elements, k=rand.randrange(1, max_elems)), ignore_index = True)
        df_res = pd.concat(rand_elems, ignore_index=True)

        # génère du bruit
        n_noise = rand.randint(min_n_noise, max_n_noise)
        rand_wls = [rand.uniform(min_wl_noise, max_wl_noise) for x in range(n_noise)] # créer en amont les valeurs de wl assure leur unicité // plus mtn mdr oups (reessayer avec sample)

        for n in range(0,n_noise):
            df_res.loc[len(df_res)] = {"wavelength": round(rand_wls[n], 1), "relint": round(rand.uniform(0, max_relint_noise), 1)} # max 1 nb après la virgule pour la wavelength et le relint

        # réordonne par wavelength
        list_df.append(df_res.sort_values("wavelength"))

    return list_df, list_labels

if __name__ == "__main__":
    path = "generation_spectre\elements"

    elements = get_elements_list(path)
    spectrum, labels = generate_spectrum(elements)
    print(labels)
    print(spectrum.info)

    # plot pour voir la gueule que ça a avec les rectangles colonnes là
    plt.plot(spectrum["wavelength"], spectrum["relint"])
    plt.show()