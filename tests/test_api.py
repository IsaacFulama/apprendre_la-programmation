import pytest
from fastapi.testclient import TestClient

from app.api.main_api import app
from app.controllers.produit_controller import get_service_produit
from app.repositories.produit_repository import DepotProduit
from app.services.produitService import ServiceProduit


@pytest.fixture
def client(tmp_path):
    depot = DepotProduit(tmp_path / "test-produits.db")
    service = ServiceProduit(depot)
    app.dependency_overrides[get_service_produit] = lambda: service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def _payload(nom="Produit test", prix=15.5, quantite=3):
    return {
        "nom": nom,
        "description": "Description test",
        "prix": prix,
        "quantite": quantite,
    }


def test_accueil(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Bienvenue sur l'API de stock"


def test_lister_produits(client):
    response = client.get("/produits")
    assert response.status_code == 200
    assert response.json() == []


def test_creer_produit_retourne_identifiant_persistant(client):
    response = client.post("/produits", json=_payload())
    assert response.status_code == 201
    produit = response.json()
    assert produit["id"] == 1
    assert produit["nom"] == "Produit test"

    reread = client.get(f"/produits/{produit['id']}")
    assert reread.status_code == 200
    assert reread.json() == produit


def test_creation_apres_suppression_ne_collisionne_pas(client):
    premier = client.post("/produits", json=_payload(nom="Premier")).json()
    deuxieme = client.post("/produits", json=_payload(nom="Deuxième")).json()
    troisieme = client.post("/produits", json=_payload(nom="Troisième")).json()

    assert client.delete(f"/produits/{premier['id']}").status_code == 200

    suivant = client.post("/produits", json=_payload(nom="Suivant"))
    assert suivant.status_code == 201
    assert suivant.json()["id"] not in {deuxieme["id"], troisieme["id"]}
    assert suivant.json()["nom"] == "Suivant"


@pytest.mark.parametrize(
    "payload",
    [
        _payload(nom="   "),
        _payload(prix=-1),
        _payload(prix=0),
        _payload(quantite=-1),
    ],
)
def test_creation_rejette_les_donnees_invalides(client, payload):
    response = client.post("/produits", json=payload)
    assert response.status_code == 422


def test_suppression_produit_absent_retourne_404(client):
    response = client.delete("/produits/999999")
    assert response.status_code == 404


def test_modification_produit_absent_retourne_404(client):
    response = client.put("/produits/999999", json=_payload())
    assert response.status_code == 404
