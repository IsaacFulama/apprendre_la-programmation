from fastapi import FastAPI

from app.controllers.produit_controller import router as produit_router

# Create the FastAPI application with a title and description.
app = FastAPI(
    title="API de stock",
    version="1.0.0",
    description="Une API simple pour apprendre FastAPI, Swagger et SQLite.",
)


# Register the product controller router.
app.include_router(produit_router)


# Return the home page message.
@app.get("/", tags=["Accueil"], summary="Page d'accueil")
def accueil():
    # Return a simple welcome message.
    return {"message": "Bienvenue sur l'API de stock"}
