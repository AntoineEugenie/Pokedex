import streamlit as st
import pandas as pd
from data_processing import load_and_clean_data
from utils import get_type_color
import plotly.express as px

st.set_page_config(page_title="Stats moyennes par type", layout="wide")
st.title("📊 Statistiques moyennes par type")

df = load_and_clean_data()


type1_df = df[['type1', 'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']].copy()
type1_df = type1_df.rename(columns={"type1": "type"})

type2_df = df[['type2', 'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']].copy()
type2_df = type2_df[type2_df['type2'] != 'None']  
type2_df = type2_df.rename(columns={"type2": "type"})

combined = pd.concat([type1_df, type2_df])

# GROUP BY
type_stats = combined.groupby("type").mean(numeric_only=True).reset_index()


type_counts = combined['type'].value_counts().reset_index() #VALUE COUNTS
type_counts.columns = ['type', 'count']


type_stats = type_stats.merge(type_counts, on="type")

st.subheader("📈 Moyennes des statistiques de combat par type")

stat_choice = st.selectbox("Choisir une statistique", ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed'])


fig = px.bar(
    type_stats.sort_values(by=stat_choice, ascending=False),
    x="type", y=stat_choice,
    color="type",
    color_discrete_map={t: get_type_color(t) for t in type_stats['type']},
    title=f"Moyenne de {stat_choice.capitalize()} par type",
)


for i, row in type_stats.iterrows():
    fig.add_annotation(
        x=row['type'], 
        y=row[stat_choice] + 1, 
        text=str(row['count']),
        font=dict(size=12, color="white"),
        showarrow=False, 
        align="center"
    )

fig.update_layout(xaxis_title="Type", yaxis_title=f"{stat_choice.capitalize()}", showlegend=False)


st.plotly_chart(fig, use_container_width=True)
