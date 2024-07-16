import pandas as pd
from StellarAnalytics.generation_spectre.randspectrum import get_elements_list, generate_spectrums
from StellarAnalytics.data_shaping import shape, pca
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from statistics import mean
from sklearn.metrics import recall_score

# parameters
max_labels_per_df = 5

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

# slice labels df in smaller dfs
list_sliced_labels = []

for i in range(len(labels.columns)//max_labels_per_df):
    list_sliced_labels.append(labels.iloc[:,i * max_labels_per_df : (i+1) * max_labels_per_df])

# add remaining columns in a last df
list_sliced_labels.append(labels.iloc[:,-(len(labels.columns) % max_labels_per_df) :])

# model integration !
prevision = pd.DataFrame()
expected = pd.DataFrame()
for df in list_sliced_labels:
    # slicing
    X_train, X_val, y_train, y_val = train_test_split(data_scaled, df.to_numpy(), test_size=0.8, random_state=42)

    # training
    model = XGBClassifier(tree_method="hist")
    model.fit(X_train, y_train)

    # predicting
    result = model.predict(X_val)
    prevision = pd.concat([prevision, pd.DataFrame(result)], axis=1)
    expected = pd.concat([expected, pd.DataFrame(y_val)], axis=1)

# precision metrics
prevision = prevision.to_numpy()
expected = expected.to_numpy()

overall_precision = [round(elem, 2) for elem in recall_score(expected, prevision, average=None)]
map(float, overall_precision)
positive_precision = []
for i in range(len(expected)):
    for j in range(len(expected[i])):
        if expected[i][j] == 1:
            positive_precision.append(prevision[i][j])

positive_precision = mean(positive_precision)

print("general accuracy score :", mean(overall_precision))
print("score by label :", overall_precision)
print("positive labels precision :", positive_precision)