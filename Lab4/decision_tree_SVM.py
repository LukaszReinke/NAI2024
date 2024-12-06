"""
authors: Łukasz Reinke
emails: s15037@pjwstk.edu.pl

============================================
PROGRAM DO KLASYFIKACJI DANYCH ABALONE I LUDNOSC
============================================

OPIS:
Ten program umożliwia klasyfikację danych ze zbiorów:
1. **Abalone** - klasyfikacja wieku ślimaka na podstawie cech fizycznych.
2. **Ludnosc** - klasyfikacja wielkości populacji w danych grupach wiekowych.

Program:
- Trenuje dwa modele klasyfikacyjne: Drzewo Decyzyjne i SVM.
- Wyświetla raporty metryk jakości klasyfikacji (precision, recall, f1-score).
- Generuje wizualizacje wybranych cech danych.
- Przewiduje wyniki dla przykładowych danych wejściowych.

"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import numpy as np

# Ścieżki do plików danych
abalone_file_path = 'abalone.csv'
ludnosc_file_path = 'ludnosc.csv'

# Wczytywanie danych
abalone_data = pd.read_csv(abalone_file_path)
ludnosc_data = pd.read_csv(ludnosc_file_path)


# --- FUNKCJE POMOCNICZE ---

def preprocess_abalone(data):
    """
    Przygotowanie danych Abalone do klasyfikacji:
    - Kodowanie płci (kolumna 'Sex').
    - Skalowanie cech.
    - Klasyfikacja: "Many Rings" (Rings > 10) lub "Few Rings" (Rings <= 10).
    """
    label_encoder = LabelEncoder()
    data['Sex'] = label_encoder.fit_transform(data['Sex'])  # Kodowanie płci
    X = data.drop(columns=['Rings'])
    y = data['Rings'].apply(lambda x: "Many Rings" if x > 10 else "Few Rings")
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    return X, y


def preprocess_ludnosc(data):
    """
    Przygotowanie danych Ludnosc do klasyfikacji:
    - Kodowanie płci (kolumna 'Płeć').
    - Skalowanie cech.
    - Klasyfikacja: "High Population" (Populacja > 100) lub "Low Population" (Populacja <= 100).
    """
    label_encoder = LabelEncoder()
    data['Płeć'] = label_encoder.fit_transform(data['Płeć'])  # Kodowanie płci
    X = data[['Lokalizacja', 'Płeć', 'Wiek']]
    y = data['Populacja'].apply(lambda x: "High Population" if x > 100 else "Low Population")
    X = pd.get_dummies(X, columns=['Lokalizacja'])  # One-hot encoding lokalizacji
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    return X, y


def train_and_evaluate(X, y, dataset_name):
    """
    Trenuj i oceń modele Drzewa Decyzyjnego i SVM na podstawie danych.
    Wyświetl raport klasyfikacyjny.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Drzewo Decyzyjne
    dt_clf = DecisionTreeClassifier(random_state=42)
    dt_clf.fit(X_train, y_train)
    dt_pred = dt_clf.predict(X_test)
    print(f"\n==== Decision Tree Classification Report for {dataset_name} ====")
    print(classification_report(y_test, dt_pred))

    # SVM
    svm_clf = SVC(random_state=42)
    svm_clf.fit(X_train, y_train)
    svm_pred = svm_clf.predict(X_test)
    print(f"\n==== SVM Classification Report for {dataset_name} ====")
    print(classification_report(y_test, svm_pred))

    return dt_clf, svm_clf


def visualize_data(data, title, x_col, y_col):
    """
    Wizualizacja danych: wykres rozproszenia dwóch wybranych kolumn.
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(data[x_col], data[y_col], alpha=0.5, c='blue')
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.grid()
    plt.show()


# --- GŁÓWNY PROGRAM ---

# Przygotowanie danych
abalone_X, abalone_y = preprocess_abalone(abalone_data)
ludnosc_X, ludnosc_y = preprocess_ludnosc(ludnosc_data)

# Trening i ocena modeli
print("=== TRENING I OCENA MODELI ===")
abalone_dt, abalone_svm = train_and_evaluate(abalone_X, abalone_y, "Abalone")
ludnosc_dt, ludnosc_svm = train_and_evaluate(ludnosc_X, ludnosc_y, "Ludnosc")

# Wizualizacja danych
visualize_data(abalone_data, "Wizualizacja danych Abalone", "Length", "Diameter")
visualize_data(ludnosc_data, "Wizualizacja danych Ludnosc", "Wiek", "Populacja")

# Przewidywanie dla przykładowych danych
example_abalone = np.array([[0, 0.5, 0.4, 0.15, 1.2, 0.6, 0.3, 0.2]])
example_ludnosc = np.zeros(ludnosc_X.shape[1])
example_ludnosc[1] = 1  # Male
example_ludnosc[-1] = 30  # Wiek

print("\n=== PRZYKŁADOWE PRZEWIDYWANIA ===")
print("Abalone Decision Tree Prediction:", abalone_dt.predict(example_abalone))
print("Abalone SVM Prediction:", abalone_svm.predict(example_abalone))
print("Ludnosc Decision Tree Prediction:", ludnosc_dt.predict([example_ludnosc]))
print("Ludnosc SVM Prediction:", ludnosc_svm.predict([example_ludnosc]))
