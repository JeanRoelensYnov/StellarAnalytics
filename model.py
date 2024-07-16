import pandas as pd
from StellarAnalytics.generation_spectre.randspectrum import get_elements_list, generate_spectrums
from StellarAnalytics.data_shaping import shape, pca
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import recall_score
from statistics import mean

# GESTION DE LA DATA
# récupère les spectres des éléments de base
print("generating elements...")
elements = get_elements_list("./StellarAnalytics/generation_spectre/elements")

# génère les spectres aléatoires + la matrice de label
print("generating spectrums...")
spectrums, labels = generate_spectrums(elements, 7000)


# transforme la liste de df en 1 df
print("shaping the data...")
data_shaped = shape(spectrums)

# scale la donnée pour limiter le nombre de colonnes
print("rescaling...")

data_scaled = pca(data_shaped, 5)

# découpe les df
X_train, X_val, y_train, y_val = train_test_split(data_scaled, labels.to_numpy(), test_size=0.8, random_state=42)

# GESTION DU MODELE

model = xgb.XGBClassifier(tree_method="hist")

# fit
print("model fitting...")
print(y_train[:5]) 
model.fit(X_train, y_train)

# predict
prediction = model.predict(X_val)

# calculate precision
overall_precision = ['%.2f' % elem for elem in recall_score(y_val, prediction, average=None)]
positive_precision = []
for i in range(len(y_val)):
    for j in range(len(y_val[i])):
        if y_val[i][j] == 1:
            positive_precision.append(prediction[i][j])
positive_precision = mean(positive_precision)

# shape result
results_expected = pd.DataFrame(y_val,columns=labels.columns)
result_chemicals = pd.DataFrame(prediction,columns=labels.columns)
result_chemicals[result_chemicals.columns] = result_chemicals[result_chemicals.columns].astype(int) # convert float to int

# save result
result_chemicals.to_csv("predictions.csv")
print("score by label :", overall_precision)
print("positive labels precision :", positive_precision)