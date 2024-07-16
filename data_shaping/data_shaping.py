import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# pour ignorer les warnings
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


# PROBLEME DE PERF :
# - shape() : trouver un moyen pour générer les colonnes manquantes du df en 1 fois (gérer les noms des colonnes ?)

def shape(list_df):
    result_df = pd.DataFrame()

    # traitement df par df
    i=0
    for df in list_df:
        i+=1
        print("traitement df ", i)
        # aplatir le df en liste de x valeurs
        data_flat = df.to_numpy().flatten()

        # ajouter des colonne au dataframe s'il n'y en a pas assez
        while len(data_flat) > len(result_df.columns):
            result_df[len(result_df.columns)] = 0
        
        # on fill avec des 0 quand des données manquent
        if len(data_flat) < len(result_df.columns):
            data_flat = np.concatenate([data_flat, [0] * (len(result_df.columns) - len(data_flat))])
        
        # ajout de la ligne
        result_df.loc[len(result_df)] = data_flat
    
    return result_df


def pca(df, nb_components):

    # min max scaler
    data_scaled = MinMaxScaler().fit(df).transform(df)

    # PCA
    result_df = PCA(n_components=nb_components).fit_transform(data_scaled)

    return result_df


def encode_labels(labels):
    le = LabelEncoder()
    data_encoded = le.fit_transform(labels)
    # on recupère l'encoder afin de 
    return data_encoded, le

def reshape(df_list):
    # stocke la donnée en np array 3D
    np_array = np.array(list(map(lambda x: x.to_numpy(), df_list)))
    print(np_array.shape)

    return np_array

def pca_2D(np_array, n):
    '''takes a 3D np array and apply PCA'''

    # flatten
    data_2d = np.array([features_2d.flatten() for features_2d in np_array])
    # min max scaler
    data_scaled = MinMaxScaler().fit(data_2d).transform(data_2d)
    # PCA
    data_pca = PCA(n_components=n).fit_transform(data_scaled)

    print("original shape:   ", data_2d.shape)
    print("transformed shape:", data_pca.shape)

    return data_pca