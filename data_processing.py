# data_processing.py
import pandas as pd
import numpy as np

def load_and_clean_data(csv_path="pokemon.csv"):
    df = pd.read_csv(csv_path)

    # Nettoyage des colonnes manquantes
    df['percentage_male'] = df['percentage_male'].fillna('Genderless')
    df['type2'] = df['type2'].fillna('None')  # on évite NaN

    # Colonne "total_stats"
    df['total_stats'] = df[['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']].sum(axis=1)

    # Colonne BMI comme exemple de nouvelle donnée
    df['bmi'] = df['weight_kg'] / (df['height_m']**2)
    df['bmi'] = df['bmi'].replace([np.inf, -np.inf], np.nan).fillna(0)

    # Format pour les types combinés
    df['types_combined'] = df.apply(lambda row: f"{row['type1']}/{row['type2']}" if row['type2'] != 'None' else row['type1'], axis=1)

    return df
