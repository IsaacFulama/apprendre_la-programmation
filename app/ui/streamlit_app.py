"""
Gestion de stock — interface Streamlit
========================================
Version enrichie : recherche/filtre, tri, alertes de stock bas, édition et
suppression de produits, export CSV, graphique de répartition, gestion
d'erreurs robuste et code mieux organisé.

Prérequis API (adapter au besoin) :
    GET    /produits            -> liste des produits
    POST   /produits             -> création
    PUT    /produits/{id}        -> mise à jour        (optionnel)
    DELETE /produits/{id}        -> suppression         (optionnel)
Si votre API ne propose pas PUT/DELETE, les boutons correspondants
afficheront simplement un message d'erreur explicite au lieu de planter.
"""

from __future__ import annotations

import io
from dataclasses import dataclass, field
from typing import Any

import pandas as pd
import requests
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

session = requests.Session()
session.trust_env = False

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------


def _get_api_url() -> str:
    try:
        return st.secrets["API_URL"]
    except (StreamlitSecretNotFoundError, KeyError):
        return "http://127.0.0.1:8002"


API_URL = _get_api_url()
TIMEOUT = 5
SEUIL_STOCK_BAS = 5  # en dessous de cette quantité, le produit est mis en évidence

st.set_page_config(page_title="Gestion de stock", page_icon="📦", layout="wide")


# --------------------------------------------------------------------------
# Couche d'accès API
# --------------------------------------------------------------------------

@dataclass
class ApiResult:
    ok: bool
    data: Any = None
    error: str = ""


def _handle_response(reponse: requests.Response) -> ApiResult:
    if reponse.ok:
        try:
            return ApiResult(True, reponse.json())
        except ValueError:
            return ApiResult(True, None)
    try:
        detail = reponse.json().get("detail", reponse.text)
    except ValueError:
        detail = reponse.text
    return ApiResult(False, error=f"Erreur {reponse.status_code} : {detail}")


def api_get(chemin: str) -> ApiResult:
    try:
        return _handle_response(session.get(f"{API_URL}{chemin}", timeout=TIMEOUT))
    except requests.RequestException as exc:
        return ApiResult(False, error=f"Erreur réseau : {exc}")


def api_post(chemin: str, payload: dict) -> ApiResult:
    try:
        return _handle_response(session.post(f"{API_URL}{chemin}", json=payload, timeout=TIMEOUT))
    except requests.RequestException as exc:
        return ApiResult(False, error=f"Erreur réseau : {exc}")


def api_put(chemin: str, payload: dict) -> ApiResult:
    try:
        return _handle_response(session.put(f"{API_URL}{chemin}", json=payload, timeout=TIMEOUT))
    except requests.RequestException as exc:
        return ApiResult(False, error=f"Erreur réseau : {exc}")


def api_delete(chemin: str) -> ApiResult:
    try:
        return _handle_response(session.delete(f"{API_URL}{chemin}", timeout=TIMEOUT))
    except requests.RequestException as exc:
        return ApiResult(False, error=f"Erreur réseau : {exc}")


# --------------------------------------------------------------------------
# État de session
# --------------------------------------------------------------------------

if "products" not in st.session_state:
    st.session_state.products: list[dict] = []
if "last_error" not in st.session_state:
    st.session_state.last_error: str | None = None
if "editing_id" not in st.session_state:
    st.session_state.editing_id: Any = None


def charger_produits() -> None:
    resultat = api_get("/produits")
    if resultat.ok:
        st.session_state.products = resultat.data or []
        st.session_state.last_error = None
    else:
        st.session_state.products = []
        st.session_state.last_error = resultat.error


def get_id(produit: dict) -> Any:
    """Récupère l'identifiant du produit quel que soit le nom du champ utilisé par l'API."""
    return produit.get("id", produit.get("_id"))


# --------------------------------------------------------------------------
# En-tête
# --------------------------------------------------------------------------

st.title("📦 Gestion de stock")
st.caption("Interface web pour consulter, ajouter, modifier et supprimer des produits")

# Chargement initial (une seule fois, pas à chaque interaction)
if not st.session_state.products and st.session_state.last_error is None:
    with st.spinner("Chargement des produits..."):
        charger_produits()


# --------------------------------------------------------------------------
# Barre latérale : ajout de produit
# --------------------------------------------------------------------------

with st.sidebar:
    st.header("➕ Ajouter un produit")
    with st.form("form_produit", clear_on_submit=True):
        nom = st.text_input("Nom *")
        description = st.text_input("Description")
        prix = st.number_input("Prix (€)", min_value=0.0, step=0.1, format="%.2f")
        quantite = st.number_input("Quantité", min_value=0, step=1)
        soumis = st.form_submit_button("Enregistrer", use_container_width=True)

        if soumis:
            erreurs = []
            if not nom.strip():
                erreurs.append("Le nom est obligatoire.")
            if prix <= 0:
                erreurs.append("Le prix doit être supérieur à 0.")

            if erreurs:
                for erreur in erreurs:
                    st.error(erreur)
            else:
                payload = {
                    "nom": nom.strip(),
                    "description": description.strip(),
                    "prix": float(prix),
                    "quantite": int(quantite),
                }
                with st.spinner("Enregistrement..."):
                    resultat = api_post("/produits", payload)
                if resultat.ok:
                    st.success(f"Produit « {nom} » ajouté avec succès.")
                    charger_produits()
                else:
                    st.error(resultat.error)

    st.divider()
    st.caption(f"🔗 API : `{API_URL}`")
    if st.button("🔄 Actualiser la liste", use_container_width=True):
        with st.spinner("Actualisation..."):
            charger_produits()


# --------------------------------------------------------------------------
# Contenu principal
# --------------------------------------------------------------------------

if st.session_state.last_error:
    st.error(f"Impossible de contacter l'API : {st.session_state.last_error}")

produits = st.session_state.products

if not produits:
    st.info("Aucun produit disponible pour le moment. Ajoutez-en un depuis le menu de gauche.")
    st.stop()

df = pd.DataFrame(produits)
for col in ("nom", "description", "prix", "quantite"):
    if col not in df.columns:
        df[col] = None

# --- Indicateurs clés ------------------------------------------------------

total_quantite = int(df["quantite"].fillna(0).sum())
valeur_totale = float((df["prix"].fillna(0) * df["quantite"].fillna(0)).sum())
nb_stock_bas = int((df["quantite"].fillna(0) < SEUIL_STOCK_BAS).sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Produits", len(df))
c2.metric("Quantité totale", total_quantite)
c3.metric("Valeur estimée", f"{valeur_totale:,.2f} €".replace(",", " "))
c4.metric("⚠️ Stock bas", nb_stock_bas, help=f"Produits avec une quantité < {SEUIL_STOCK_BAS}")

if nb_stock_bas:
    st.warning(f"{nb_stock_bas} produit(s) sous le seuil de stock ({SEUIL_STOCK_BAS} unités).")

st.divider()

# --- Recherche, filtre et tri ----------------------------------------------

f1, f2, f3 = st.columns([2, 1, 1])
with f1:
    recherche = st.text_input("🔍 Rechercher un produit", placeholder="Nom ou description...")
with f2:
    tri_par = st.selectbox("Trier par", ["nom", "prix", "quantite"], format_func=str.capitalize)
with f3:
    ordre_desc = st.checkbox("Ordre décroissant")

df_affiche = df.copy()
if recherche:
    masque = (
        df_affiche["nom"].astype(str).str.contains(recherche, case=False, na=False)
        | df_affiche["description"].astype(str).str.contains(recherche, case=False, na=False)
    )
    df_affiche = df_affiche[masque]

df_affiche = df_affiche.sort_values(by=tri_par, ascending=not ordre_desc, na_position="last")

st.caption(f"{len(df_affiche)} produit(s) affiché(s) sur {len(df)}")

# --- Tableau + export --------------------------------------------------

colonnes_utiles = [c for c in ["nom", "description", "prix", "quantite"] if c in df_affiche.columns]
st.dataframe(
    df_affiche[colonnes_utiles],
    use_container_width=True,
    hide_index=True,
    column_config={
        "prix": st.column_config.NumberColumn("Prix", format="%.2f €"),
        "quantite": st.column_config.NumberColumn("Quantité"),
    },
)

csv_buffer = io.StringIO()
df_affiche[colonnes_utiles].to_csv(csv_buffer, index=False)
st.download_button(
    "⬇️ Exporter en CSV",
    data=csv_buffer.getvalue(),
    file_name="produits.csv",
    mime="text/csv",
)

st.divider()

# --- Répartition visuelle ---------------------------------------------

if df_affiche["quantite"].notna().any():
    st.subheader("📊 Répartition des quantités par produit")
    chart_df = df_affiche.set_index("nom")["quantite"]
    st.bar_chart(chart_df)

st.divider()

# --- Modification / suppression -----------------------------------------

st.subheader("✏️ Modifier ou supprimer un produit")

for _, row in df_affiche.iterrows():
    produit = row.to_dict()
    pid = get_id(produit)
    label = f"{produit.get('nom', 'Produit')} — {produit.get('quantite', 0)} unité(s)"

    with st.expander(label):
        if st.session_state.editing_id == pid:
            with st.form(f"edit_form_{pid}"):
                nom_e = st.text_input("Nom", value=produit.get("nom", ""))
                desc_e = st.text_input("Description", value=produit.get("description", ""))
                prix_e = st.number_input(
                    "Prix (€)", min_value=0.0, step=0.1, format="%.2f",
                    value=float(produit.get("prix") or 0),
                )
                qte_e = st.number_input(
                    "Quantité", min_value=0, step=1, value=int(produit.get("quantite") or 0),
                )
                col_ok, col_cancel = st.columns(2)
                valider = col_ok.form_submit_button("💾 Enregistrer", use_container_width=True)
                annuler = col_cancel.form_submit_button("Annuler", use_container_width=True)

                if valider:
                    if pid is None:
                        st.error("Cette API ne renvoie pas d'identifiant : impossible de modifier ce produit.")
                    else:
                        payload = {
                            "nom": nom_e.strip(),
                            "description": desc_e.strip(),
                            "prix": float(prix_e),
                            "quantite": int(qte_e),
                        }
                        resultat = api_put(f"/produits/{pid}", payload)
                        if resultat.ok:
                            st.success("Produit mis à jour.")
                            st.session_state.editing_id = None
                            charger_produits()
                            st.rerun()
                        else:
                            st.error(resultat.error)
                if annuler:
                    st.session_state.editing_id = None
                    st.rerun()
        else:
            col_info, col_edit, col_del = st.columns([3, 1, 1])
            with col_info:
                st.write(produit.get("description") or "_Pas de description_")
                st.write(f"**Prix :** {produit.get('prix', 0):.2f} €")
            with col_edit:
                if st.button("Modifier", key=f"edit_{pid}", use_container_width=True):
                    st.session_state.editing_id = pid
                    st.rerun()
            with col_del:
                if st.button("🗑️ Supprimer", key=f"del_{pid}", use_container_width=True):
                    if pid is None:
                        st.error("Cette API ne renvoie pas d'identifiant : impossible de supprimer ce produit.")
                    else:
                        resultat = api_delete(f"/produits/{pid}")
                        if resultat.ok:
                            st.success("Produit supprimé.")
                            charger_produits()
                            st.rerun()
                        else:
                            st.error(resultat.error)