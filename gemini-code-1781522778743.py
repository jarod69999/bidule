import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Générateur de Classement", page_icon="🏆")

# 1. Le choix de la question
question = st.text_input(
    "Quelle est ta question ?", 
    value="Qui est le meilleur au volley ?"
)

st.title(question)
st.write("Modifie la colonne 'Rang' pour classer les personnes (1 = le meilleur) :")

# Liste de l'équipe
personnes = ["Pierric", "Anna", "Antoine", "Emmanuel", "Tatou", "Jarod"]

# Initialisation des données dans la session
if 'df_classement' not in st.session_state:
    st.session_state.df_classement = pd.DataFrame({
        "Personne": personnes,
        "Rang": [i+1 for i in range(len(personnes))]
    })

# 2. L'interface de classement (tableau éditable)
df_edited = st.data_editor(
    st.session_state.df_classement,
    column_config={
        "Rang": st.column_config.NumberColumn(
            "Rang",
            help="Choisis la position (1 à 6)",
            min_value=1,
            max_value=len(personnes),
            step=1,
        )
    },
    disabled=["Personne"], # Empêche de modifier les noms
    hide_index=True,
    use_container_width=True
)

# 3. L'affichage du résultat final
if st.button("Valider le classement"):
    st.divider()
    st.subheader("🏆 Classement final :")
    
    # Tri dans l'ordre croissant selon le rang
    df_sorted = df_edited.sort_values(by="Rang", ascending=True).reset_index(drop=True)
    
    # Affichage du top
    for index, row in df_sorted.iterrows():
        st.markdown(f"**{int(row['Rang'])}.** {row['Personne']}")