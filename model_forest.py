import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from statistics import mean
from sklearn.metrics import recall_score

# parameters
max_labels_per_df = 5

# load data from csv

print("loading data...")

data_scaled = np.genfromtxt("spectrums_after_pca2.csv", delimiter=",")
labels = pd.read_csv("labels2.csv")

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

print(prevision.head(5))
print(expected.head(5))

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