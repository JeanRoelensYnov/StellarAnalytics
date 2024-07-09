import pandas as pd
import numpy as np

# ACTUELLEMENT  :
# ne gère pas la cahérence données -> label, mais que les données numériques
# il faudra choisir quand le lien sera fait (avant ? pendant ?)


def shape(list_df):
    result_df = pd.DataFrame()

    # traitemetn df par df
    for df in list_df:
        # aplatir le df en liste de x valeurs
        data_flat = df.to_numpy().flatten()

        # ajouter des colonne au dataframe s'il n'y en a pas assez
        while len(data_flat) > len(result_df.columns):
            result_df[len(result_df.columns)] = np.nan
            print("columns +1")
        
        # si la liste a moins de valeurs que le df de colonnes, on y rajoute des nan :
        if len(data_flat) < len(result_df.columns):
            data_flat = np.concatenate([data_flat, [np.nan] * (len(result_df.columns) - len(data_flat))])
        
        # ajout de la ligne
        result_df.loc[len(result_df)] = data_flat
    
    return result_df

def pca():
    
    pass