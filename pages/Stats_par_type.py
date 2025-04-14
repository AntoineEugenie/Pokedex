import streamlit as st
import pandas as pd
from data_processing import load_and_clean_data
from utils import get_type_color
import plotly.express as px

st.set_page_config(page_title="Stats moyennes par type", layout="wide")
st.title("📊 Statistiques moyennes par type")

# Chargement des données
df = load_and_clean_data()

# Dupliquer les Pokémon à double type pour les compter dans les deux catégories
type1_df = df[['type1', 'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']].copy()
type1_df = type1_df.rename(columns={"type1": "type"})

type2_df = df[['type2', 'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']].copy()
type2_df = type2_df[type2_df['type2'] != 'None']  # Exclure les types secondaires vides
type2_df = type2_df.rename(columns={"type2": "type"})

combined = pd.concat([type1_df, type2_df])

# Moyenne par type
type_stats = combined.groupby("type").mean(numeric_only=True).reset_index()

# Affichage graphique
st.subheader("📈 Moyennes des statistiques de combat par type")

# Choix de la stat à visualiser
stat_choice = st.selectbox("Choisir une statistique", ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed'])

fig = px.bar(
    type_stats.sort_values(by=stat_choice, ascending=False),
    x="type", y=stat_choice,
    color="type",
    color_discrete_map={t: get_type_color(t) for t in type_stats['type']},
    title=f"Moyenne de {stat_choice.capitalize()} par type",
)
fig.update_layout(xaxis_title="Type", yaxis_title=f"{stat_choice.capitalize()}", showlegend=False)

st.plotly_chart(fig, use_container_width=True)
