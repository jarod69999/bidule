import streamlit as st
import pandas as pd
import json
import os

# Fichier pour sauvegarder les données de la communauté
DATA_FILE = "communaute_data.json"

# Fonctions pour lire et sauvegarder les données
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"rankings": {}, "comments": {}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Configuration de la page
st.set_page_config(page_title="Classement de l'équipe", page_icon="🔥")

# Chargement de la base de données locale
data = load_data()

st.title("🔥 Les Classements de l'équipe")

# 1. Identification obligatoire
utilisateur = st.text_input("Comment tu t'appelles ?", placeholder="Ton prénom (ex: Jarod)...")

if not utilisateur:
    st.warning("Entre ton nom pour participer et voir les classements.")
    st.stop()

st.divider()

# 2. Choix ou Création de la question
questions_existantes = list(data["rankings"].keys())
options = ["-- Nouvelle question --"] + questions_existantes

choix_q = st.selectbox("Sélectionne un thème ou crée-en un nouveau :", options)

if choix_q == "-- Nouvelle question --":
    question = st.text_input("Tape ta nouvelle question :", placeholder="ex: Qui a le meilleur style vestimentaire ?")
else:
    question = choix_q

if not question:
    st.info("Sélectionne ou tape une question pour continuer.")
    st.stop()

# Initialiser la question dans les données si elle est nouvelle
if question not in data["rankings"]:
    data["rankings"][question] = {}
if question not in data["comments"]:
    data["comments"][question] = []

# 3. Interface de vote (spécifique à l'utilisateur)
st.subheader(f"Ton classement pour : {question}")
personnes = ["Pierric", "Anna", "Antoine", "Emmanuel", "Tatou", "Jarod"]

# Si l'utilisateur a déjà voté, on affiche son classement précédent
if utilisateur in data["rankings"][question]:
    classement_actuel = data["rankings"][question][utilisateur]
    df_init = pd.DataFrame({
        "Personne": classement_actuel,
        "Rang": [i+1 for i in range(len(classement_actuel))]
    })
else:
    df_init = pd.DataFrame({
        "Personne": personnes,
        "Rang": [i+1 for i in range(len(personnes))]
    })

# Tableau éditable
df_edited = st.data_editor(
    df_init,
    column_config={
        "Rang": st.column_config.NumberColumn(
            "Rang (1 = le meilleur)", 
            min_value=1, 
            max_value=len(personnes), 
            step=1
        )
    },
    disabled=["Personne"],
    hide_index=True,
    key=f"editor_{question}"
)

if st.button("Valider mon classement"):
    # On trie selon les rangs modifiés par l'utilisateur
    df_sorted = df_edited.sort_values(by="Rang", ascending=True)
    classement_final = df_sorted["Personne"].tolist()
    
    # On sauvegarde dans le JSON
    data["rankings"][question][utilisateur] = classement_final
    save_data(data)
    st.success("Classement enregistré !")
    st.rerun()

st.divider()

# 4. Affichage des classements de la communauté
st.subheader("👀 Ce que les autres ont voté")
if not data["rankings"][question]:
    st.write("Personne n'a encore voté pour cette question.")
else:
    # Affichage en colonnes pour que ce soit propre
    cols = st.columns(3)
    for i, (user, rank_list) in enumerate(data["rankings"][question].items()):
        with cols[i % 3]:
            st.markdown(f"**De {user}**")
            for pos, nom in enumerate(rank_list, 1):
                st.text(f"{pos}. {nom}")

st.divider()

# 5. Espace Commentaires
st.subheader("💬 Espace Commentaires")

# Affichage de l'historique des commentaires
for c in data["comments"][question]:
    st.markdown(f"**{c['user']}** : {c['text']}")

# Ajout d'un commentaire
nouveau_com = st.text_input("Réagis au classement...")
if st.button("Envoyer"):
    if nouveau_com:
        data["comments"][question].append({"user": utilisateur, "text": nouveau_com})
        save_data(data)
        st.rerun()
