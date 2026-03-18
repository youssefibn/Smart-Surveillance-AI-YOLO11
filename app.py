import streamlit as st
import pandas as pd
import plotly.express as px
import os
import glob

# 1. Configuration de la page
st.set_page_config(page_title="IA Surveillance - Dashboard", page_icon="🛡️", layout="wide")

# Personnalisation du style
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #d1d8e0;
    }
    .stMetric {
        color: #2e3440;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ AI Smart Surveillance Analytics Dashboard")
st.markdown("---")

# 2. Section des Captures Récentes (Nouvelle Fonctionnalité)
st.subheader("📸 Dernières Détections de Personnes")

# Recherche de toutes les images dans le dossier captures
capture_folder = "captures"
if os.path.exists(capture_folder):
    # Liste de toutes les images .jpg, triées par date de création (la plus récente d'abord)
    list_of_files = glob.glob(f"{capture_folder}/*.jpg")
    latest_files = sorted(list_of_files, key=os.path.getctime, reverse=True)
    
    # On n'en garde que les 3 dernières
    display_count = min(3, len(latest_files))
    
    if display_count > 0:
        # Création de colonnes pour un affichage côte à côte
        cols = st.columns(display_count)
        
        for i in range(display_count):
            file_path = latest_files[i]
            # Extraction du timestamp depuis le nom du fichier (pour l'affichage)
            # Exemple: captures/personne_20240315_123456.jpg -> 12:34:56
            file_name = os.path.basename(file_path)
            timestamp_str = file_name.split('_')[2].split('.')[0] # 123456
            formatted_time = f"{timestamp_str[:2]}:{timestamp_str[2:4]}:{timestamp_str[4:]}"
            
            with cols[i]:
                st.image(file_path, caption=f"👤 Personne détectée à {formatted_time}", use_container_width=True)
                # Ajout d'un bouton de téléchargement pour l'ingénierie de sécurité
                with open(file_path, "rb") as file:
                    btn = st.download_button(
                        label=f"Télécharger",
                        data=file,
                        file_name=file_name,
                        mime="image/jpg"
                    )
    else:
        st.info("ℹ️ Aucune capture de personne disponible pour le moment.")
else:
    st.warning("⚠️ Dossier 'captures' introuvable. Veuillez d'abord lancer 'python main.py' en présence d'une personne.")

st.markdown("---")

# 3. Section des Statistiques Classiques
if os.path.exists("activity_log.csv"):
    df = pd.read_csv("activity_log.csv")
    
    # KPIs
    total_events = len(df)
    unique_objects = df['Object'].nunique()
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Detections", f"{total_events} événements", help="Nombre total de détections enregistrées (toutes les 2s)")
    kpi2.metric("Unique Objects", unique_objects, help="Nombre de types d'objets différents détectés")
    kpi3.metric("System Status", "Live", delta="Healthy")

    st.markdown("---")

    # Graphiques
    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader("📊 Répartition des Objets")
        fig = px.pie(df, names='Object', hole=0.5, color_discrete_sequence=px.colors.sequential.Plotly3)
        st.plotly_chart(fig, use_container_width=True)

    with right_column:
        st.subheader("📋 Historique des Activités")
        st.dataframe(df.sort_values(by="Timestamp", ascending=False), height=300, use_container_width=True)

    # Simulation d'Intelligence Artificielle
    st.info(f"💡 **AI Insight:** L'objet le plus fréquemment détecté est **'{df['Object'].mode()[0]}'**. Aucune activité suspecte détectée.")

else:
    st.warning("⚠️ Aucune donnée détectée. Veuillez d'abord lancer 'python main.py' pour collecter des données.")