from fastapi import FastAPI

from app.controllers.categorie_controller import router as categorie_router
from app.controllers.client_controller import router as client_router
from app.controllers.facture_controller import router as facture_router
from app.controllers.fournisseur_controller import router as fournisseur_router
from app.controllers.produit_controller import router as produit_router
from app.controllers.stock_controller import router as stock_router
from app.controllers.vente_controller import router as vente_router

app = FastAPI(
    title="API de stock",
    version="1.0.0",
    description="Une API simple pour apprendre FastAPI, Swagger et SQLite.",
)

app.include_router(produit_router)
app.include_router(client_router)
app.include_router(facture_router)
app.include_router(categorie_router)
app.include_router(fournisseur_router)
app.include_router(stock_router)
app.include_router(vente_router)


@app.get("/", tags=["Accueil"], summary="Page d'accueil")
def accueil():
    return {"message": "Bienvenue sur l'API de stock"}
