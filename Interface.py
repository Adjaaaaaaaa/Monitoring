import os

import requests
import streamlit as st

st.set_page_config(page_title="Prédiction Gravité Accident", layout="centered")

st.title("Prédiction de la Gravité d'un Accident")
st.write("Saisissez les caractéristiques de l'accident pour estimer sa gravité.")

# 1. Formulaire avec noms complets (correspondant à AccidentData dans l'API)
with st.form("accident_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Âge de l'usager", min_value=0, max_value=100, value=30)
        vma = st.number_input(
            "Vitesse maximale autorisée (km/h)", min_value=1, max_value=130, value=50
        )
        nbv = st.number_input("Nombre de voies", min_value=1, max_value=10, value=2)
        sexe = st.checkbox("L'usager est-il un homme ?", value=True)

    with col2:
        secu = st.checkbox("Ceinture ou casque attaché ?", value=True)
        agglo = st.checkbox("En agglomération ?", value=True)
        col_front = st.checkbox("Collision frontale ?", value=False)
        nuit = st.checkbox("Pleine nuit sans éclairage ?", value=False)
        meteo = st.checkbox("Météo normale (soleil/nuages) ?", value=True)

    submit = st.form_submit_button("Prédire la gravité")

# 2. Logique d'appel à l'API
if submit:
    # On prépare le dictionnaire avec les noms de clés attendus par models.py
    payload = {
        "age_usager": age,
        "vitesse_max_autorisee": vma,
        "nombre_de_voies": nbv,
        "ceinture_ou_casque_attache": secu,
        "en_agglomeration": agglo,
        "collision_frontale": col_front,
        "sexe_masculin": sexe,
        "luminosite_pleine_nuit": nuit,
        "meteo_normale": meteo,
    }

    try:
        # Remplacez l'URL si votre API est sur un autre port

        # Utilisation de l'URL Docker
        api_url = os.getenv("API_URL", "http://127.0.0.1:8000")
        response = requests.post(f"{api_url}/predict", json=payload)

        if response.status_code == 200:
            result = response.json()

            # 3. Affichage du résultat
            st.subheader(f"Résultat : {result['label_francais']}")

            # Couleur en fonction du code gravité
            colors = {1: "green", 2: "red", 3: "orange", 4: "blue"}
            color = colors.get(result["gravite_code"], "black")

            st.markdown(f"**Code Gravité :** :{color}[{result['gravite_code']}]")

            # Affichage des probabilités
            st.write("### Détail des probabilités :")
            for label, prob in result["probabilites"].items():
                st.write(f"- {label} : {prob * 100:.2f}%")
                st.progress(prob)

        else:
            st.error(f"Erreur API ({response.status_code}) : {response.text}")

    except Exception as e:
        st.error(
            f"Impossible de contacter l'API. Vérifiez qu'elle est lancée. Erreur : {e}"
        )
