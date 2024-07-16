import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import recall_score
from statistics import mean

# recuperation des données
print("loading data...")

data_scaled = np.genfromtxt("scaled_data.csv", delimiter=",")
labels = pd.read_csv("related_labels.csv")

X_train, X_val, y_train, y_val = train_test_split(data_scaled, labels.to_numpy(), test_size=0.8, random_state=42)



# intégration du modèle

model = xgb.XGBClassifier(tree_method="hist")

# fit

print("model fitting...")

model.fit(X_train, y_train)

# predict

prediction = model.predict(X_val)


# calculate precision

overall_precision = [round(elem, 2) for elem in recall_score(y_val, prediction, average=None)]
map(float, overall_precision)
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

print(result_chemicals.head(5))
print(results_expected.head(5))

print("general score :", mean(overall_precision))
print("score by label :", overall_precision)
print("positive labels precision :", positive_precision)