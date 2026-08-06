import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Gestion de stock", page_icon="📦", layout="wide")
st.title("📦 Gestion de stock")
st.caption("Interface web simple pour consulter et ajouter des produits")

if "products" not in st.session_state:
    st.session_state.products = []


def charger_produits():
    try:
        reponse = requests.get(f"{API_URL}/produits", timeout=5)
        if reponse.status_code == 200:
            st.session_state.products = reponse.json()
        else:
            st.session_state.products = []
    except requests.RequestException:
        st.session_state.products = []


with st.sidebar:
    st.header("Ajouter un produit")
    with st.form("form_produit"):
        nom = st.text_input("Nom")
        description = st.text_input("Description")
        prix = st.number_input("Prix", min_value=0.0, step=0.1)
        quantite = st.number_input("Quantité", min_value=0, step=1)
        soumis = st.form_submit_button("Enregistrer")

        if soumis:
            payload = {
                "nom": nom,
                "description": description,
                "prix": float(prix),
                "quantite": int(quantite),
            }
            try:
                reponse = requests.post(f"{API_URL}/produits", json=payload, timeout=5)
                if reponse.status_code == 200:
                    st.success("Produit ajouté avec succès")
                    st.session_state.products = []
                else:
                    st.error("Échec de l'ajout du produit")
            except requests.RequestException as exc:
                st.error(f"Erreur réseau : {exc}")

st.button("Actualiser", on_click=charger_produits)
charger_produits()

if st.session_state.products:
    st.dataframe(st.session_state.products, use_container_width=True)
else:
    st.info("Aucun produit disponible pour le moment.")
