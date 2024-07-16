import pandas as pd
import numpy as np
from generation_spectre.randspectrum import get_elements_list, new_generate_spectrums
from data_shaping import reshape, pca_2D


# GESTION DE LA DATA

# récupère les spectres des éléments de base

print("generating elements...")
elements = get_elements_list("./generation_spectre/elements")

# génère les spectres aléatoires + la matrice de label

print("generating spectrums...")
spectrums, labels = new_generate_spectrums(elements, 1000, 0.1)

# transforme la liste de df en np array 3D

print("shaping the data...")
data_shaped = reshape(spectrums)

# scale la donnée pour limiter le nombre de colonnes

print("rescaling...")
data_scaled = pca_2D(data_shaped, 5)


# enregistre sous csv pour eviter d'avoir a regénérer les spectres
print("saving to csv...")
np.savetxt("scaled_data.csv", data_scaled, delimiter=",")
labels.to_csv("related_labels.csv", index=False)