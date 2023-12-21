import pandas as pd
import numpy as np

from enum import Enum
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.base import clone
import joblib

import matplotlib.pyplot as plt
import seaborn as sns

class Algorithm(Enum):
    RANDOM_FOREST = "RandomForest"

class MachineLearningProduce:

    def __init__(self, algorithm, model):
        if algorithm not in Algorithm:
            raise ValueError("Algoritma tidak ada")
        self.algorithm = algorithm
        self.model = model

    # def data_cleaning_preprocessing(self, df, log_features, categorical_features):
    #     df_cleaned = df.dropna(axis=0).copy()

    #     for feature in log_features:
    #         if feature == 'person_age':
    #             df_cleaned['person_age'] = np.log1p(df_cleaned['person_age'])
    #         elif feature == 'person_emp_length':
    #             df_cleaned['person_emp_length'] = np.log1p(df_cleaned['person_emp_length'])

    #     for feature in categorical_features:
    #         if feature == 'person_home_ownership':
    #             df_cleaned.person_home_ownership = df_cleaned.person_home_ownership.replace(["RENT", "MORTGAGE", "OWN", "OTHER"], [1, 2, 3, 4])
    #         elif feature == 'loan_intent':
    #             df_cleaned.loan_intent = df_cleaned.loan_intent.replace(["EDUCATION", "MEDICAL", "VENTURE", "PERSONAL", "DEBTCONSOLIDATION", "HOMEIMPROVEMENT"], [1, 2, 3, 4, 5, 6])
    #         elif feature == 'loan_grade':
    #             df_cleaned.loan_grade = df_cleaned.loan_grade.replace(["A", "B", "C", "D", "E", "F", "G"], [1, 2, 3, 4, 5, 6, 7])
    #         else:
    #             df_cleaned.cb_person_default_on_file = df_cleaned.cb_person_default_on_file.replace(["N", "Y"], [0, 1])

    #     return df_cleaned
        
    def data_cleaning_preprocessing(self, df, log_features, categorical_features):
        df_cleaned = df.dropna(axis=0).copy()

        for feature in log_features:
            if feature == 'person_age' and 'person_age' in df_cleaned.columns:
                df_cleaned['person_age'] = np.log1p(df_cleaned['person_age'])
            elif feature == 'person_emp_length' and 'person_emp_length' in df_cleaned.columns:
                df_cleaned['person_emp_length'] = np.log1p(df_cleaned['person_emp_length'])

        for feature in categorical_features:
            if feature == 'person_home_ownership' and 'person_home_ownership' in df_cleaned.columns:
                df_cleaned.person_home_ownership = df_cleaned.person_home_ownership.replace(["RENT", "MORTGAGE", "OWN", "OTHER"], [1, 2, 3, 4])
            elif feature == 'loan_intent' and 'loan_intent' in df_cleaned.columns:
                df_cleaned.loan_intent = df_cleaned.loan_intent.replace(["EDUCATION", "MEDICAL", "VENTURE", "PERSONAL", "DEBTCONSOLIDATION", "HOMEIMPROVEMENT"], [1, 2, 3, 4, 5, 6])
            elif feature == 'loan_grade' and 'loan_grade' in df_cleaned.columns:
                df_cleaned.loan_grade = df_cleaned.loan_grade.replace(["A", "B", "C", "D", "E", "F", "G"], [1, 2, 3, 4, 5, 6, 7])
            elif feature == 'cb_person_default_on_file' and 'cb_person_default_on_file' in df_cleaned.columns:
                df_cleaned.cb_person_default_on_file = df_cleaned.cb_person_default_on_file.replace(["N", "Y"], [0, 1])

        return df_cleaned

    def cross_validation(self, X, y, cv=5):
        if self.model is None:
            raise ValueError("Model belum diinisialisasi. Gunakan metode train_model terlebih dahulu.")

        accuracy_scores = cross_val_score(self.model, X, y, cv=cv, scoring='accuracy')
        precision_scores = cross_val_score(self.model, X, y, cv=cv, scoring='precision')
        recall_scores = cross_val_score(self.model, X, y, cv=cv, scoring='recall')
        f1_scores = cross_val_score(self.model, X, y, cv=cv, scoring='f1')

        return accuracy_scores, precision_scores, recall_scores, f1_scores
    
    def train_model(self, model, X_train, y_train):
        model.fit(X_train, y_train)
    
    def make_predict(self, model, X_test):
        if self.algorithm == Algorithm.RANDOM_FOREST:
            predictions = model.predict(X_test)
            return predictions
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")


    def saved_model(self, model, file_path):
        joblib.dump(model, file_path)