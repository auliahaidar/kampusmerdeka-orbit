# -*- coding: utf-8 -*-
"""Iris Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P7XYpxfTPTZXpcsi-PgoiIn6CoAwgLPF

# Klasifikasi Bunga Iris
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

df = pd.read_csv("sample_data/weight-height.xlsx")
df.drop('Id', axis=1, inplace=True)

df.head()

"""## Scaling dan Labeling Atribut"""

std_scaler = StandardScaler()
label_enc = LabelEncoder()

df.iloc[:, :-1] = std_scaler.fit_transform(df.iloc[:, :-1])
df.Species = label_enc.fit_transform(df.Species)

df.head()

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

"""## Training Model"""

log_regr = LogisticRegression()
X_train, X_test, y_train, y_test = train_test_split(X, y)

model = log_regr.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

print(f"Akurasi Model: {accuracy * 100}%")

"""## Menyimpan Model dan Scaler"""

joblib.dump((model, std_scaler), "iris-classification-using-logistic-regression.pkl")