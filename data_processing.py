import pandas as pd
import numpy as np

def load_and_clean_data(csv_path="pokemon.csv"):
    df = pd.read_csv(csv_path)

    df['percentage_male'] = df['percentage_male'].fillna('Genderless')
    df['type2'] = df['type2'].fillna('None') 
    # SUM
    df['total_stats'] = df[['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']].sum(axis=1)

    # ASSIGN
    df = df.assign(bmi=df['weight_kg'] / (df['height_m']**2)).replace([np.inf, -np.inf], np.nan).fillna(0)

    # APPLY
    df['types_combined'] = df.apply(lambda row: f"{row['type1']}/{row['type2']}" if row['type2'] != 'None' else row['type1'], axis=1)

    return df
