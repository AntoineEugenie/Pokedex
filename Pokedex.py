import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.parse
from data_processing import load_and_clean_data
from utils import get_type_color, create_type_gradient
import plotly.graph_objects as go
import google.generativeai as genai
import json


st.set_page_config(page_title="Pokédex", layout="wide")

genai.configure(api_key="AIzaSyBowUaTFOxPKM_j0DvXUxz75m-TnoEOrDA")


model = genai.GenerativeModel("gemini-2.0-flash") 

st.title("📘 Pokédex National 7G (les bons jeu en gros)")

df = load_and_clean_data()

question = st.text_input("Pose une question au professeur :")


data = df.to_dict(orient="records")

if st.button("Demander au professeur Dilion"):
    prompt = f"""Tu es le professeur Dilion expert en Pokémon. Voici des données extraites du Pokédex (7G) :
    
{json.dumps(data)}

Réponds de manière concise, claire et pédagogique à la question suivante :

{question}
"""
    with st.spinner("Le professeur réfléchit..."):
        response = model.generate_content(prompt)
        st.markdown(f"🧑‍🏫 **Professeur** : {response.text}")

selected_name = st.query_params.get("pokemon")
if selected_name:
    selected_name = urllib.parse.unquote(selected_name)  
    selected_name = selected_name.strip().lower()  
    match = df[df['name'].str.strip().str.lower() == selected_name]

    if not match.empty:
        selected_pokemon = match.iloc[0]

        st.markdown("⬅️ [Retour au Pokédex](./)")
        st.header(f"{selected_pokemon['name']} – {selected_pokemon['types_combined']}")

        col1, col2 = st.columns(2)

        

        with col1:
            st.subheader("📊 Statistiques de combat")

            stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']

            
            stats_df = pd.DataFrame({
                'Stat': stats,
                'Valeur': [selected_pokemon[stat] for stat in stats]
            })

           
            fig = px.line_polar(stats_df, r='Valeur', theta='Stat', line_close=True,
                                template='plotly_dark', line_shape='linear')

            fig.update_traces(fill='toself', line_color='royalblue')
            fig.update_layout(polar=dict(
                radialaxis=dict(visible=True, range=[0, 260])
            ))

            st.plotly_chart(fig, use_container_width=True)
            

            


        with col2:
            
            ivm = selected_pokemon[['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']].mean()
            ivm_color = "🟢 Élevé" if ivm > 100 else "🟡 Moyen" if ivm > 70 else "🔴 Faible"

            st.subheader("📋 Informations")
            st.markdown(f"""
             Pokémon {"légendaire" if selected_pokemon['is_legendary'] else "commun"}
            - **Classification** : {selected_pokemon['classfication']}
            - **IVM** : {ivm:.1f} – {ivm_color}
            - **Total stats** : {selected_pokemon['total_stats']}
            - **Taille** : {selected_pokemon['height_m']} m
            - **Poids** : {selected_pokemon['weight_kg']} kg
            - **BMI** : {format(selected_pokemon['bmi'],'.2f')} 
            - **Taux de capture** : {selected_pokemon['capture_rate']}
            - **Bonheur de base** : {selected_pokemon['base_happiness']}
            {"- **Genre** : Non genré"  if selected_pokemon['percentage_male']== "Genderless" else f"- **Genre** : Male {format(selected_pokemon['percentage_male'],'.2f')}%,  Femelle {format(100 - selected_pokemon['percentage_male'],'.2f')}%"}
            """)
            
            # Récupération et préparation des résistances
            against_cols = [col for col in df.columns if col.startswith('against_')]
            resistances = selected_pokemon[against_cols].astype(float)
            types = [col.replace("against_", "") for col in against_cols]

            # Création de la heatmap Plotly
            fig = go.Figure(data=go.Heatmap(
                z=[resistances.values],
                x=types,
                
                colorscale='RdBu',
                zmin=0,
                zmax=2,
                text=[[f"{val:.2f}" for val in resistances.values]],
                hoverinfo="text"
            ))

            fig.update_layout(
                title="🧪 Résistances par type",
                height=200,
                margin=dict(l=10, r=10, t=30, b=10)
            )

            st.plotly_chart(fig, use_container_width=True)
            
        st.stop()
    else:
        st.error("Pokémon introuvable ! Le lien est peut-être invalide ou le nom contient des caractères spéciaux.")



# Sidebar - Filtres
st.sidebar.header("🔎 Filtres")
name_filter = st.sidebar.text_input("Nom contient...")
type_filter = st.sidebar.multiselect("Type", sorted(set(df['type1']) | set(df['type2'])))


# Application des filtres
filtered_df = df.copy()
if name_filter:
    filtered_df = filtered_df[filtered_df['name'].str.contains(name_filter, case=False)]

if type_filter:
    filtered_df = filtered_df[(filtered_df['type1'].isin(type_filter)) | (filtered_df['type2'].isin(type_filter))]

# Tri
sort_column = st.sidebar.selectbox("Trier par", ['pokedex_number' ,'name','height_m','weight_kg', 'hp', 'attack', 'defense','sp_attack','sp_defense','speed', 'total_stats'])
sort_ascending = st.sidebar.checkbox("Ordre croissant", True)
filtered_df = filtered_df.sort_values(by=sort_column, ascending=sort_ascending)


# Affichage des cartes
cols = st.columns(4)
for idx, (_, row) in enumerate(filtered_df.iterrows()):
    with cols[idx % 4]:
        type1 = row['type1']
        type2 = row['type2']
        bg_color = create_type_gradient(type1, type2) if type2 != 'None' else get_type_color(type1)

        st.markdown(f"""
                    <a href="?pokemon={row['name']}" style="color: white; text-decoration: none;">
        <div style="background: {bg_color}; padding: 10px; border-radius: 10px; margin-bottom: 10px; color: white">
            <div style="font-size: 20px; font-weight: bold;">#{row['pokedex_number']} {row['name']}</a></div>
            <p>Types: {row['types_combined']}</p>
        </div>
        """, unsafe_allow_html=True)
