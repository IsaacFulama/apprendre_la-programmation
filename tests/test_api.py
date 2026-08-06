# Import the test client from FastAPI.
from fastapi.testclient import TestClient

# Import the FastAPI application.
from app.api.main_api import app

# Create one client instance for the whole test file.
client = TestClient(app)


# Test the home route.
def test_accueil():
    # Send a GET request to the home page.
    reponse = client.get("/")
    # The response should be successful.
    assert reponse.status_code == 200
    # The response body should contain the expected welcome message.
    assert reponse.json()["message"] == "Bienvenue sur l'API de stock"


# Test the route that lists products.
def test_lister_produits():
    # Send a GET request to list the products.
    reponse = client.get("/produits")
    # The response should be successful.
    assert reponse.status_code == 200
    # The response body should be a list.
    assert isinstance(reponse.json(), list)


# Test the route that creates a product.
def test_creer_produit():
    # Build a payload with a product example.
    payload = {
        "nom": "Produit test",
        "description": "Description test",
        "prix": 15.5,
        "quantite": 3,
    }
    # Send a POST request with the payload.
    reponse = client.post("/produits", json=payload)
    # The request should succeed.
    assert reponse.status_code == 200
    # The created product should have the provided name.
    assert reponse.json()["nom"] == "Produit test"
