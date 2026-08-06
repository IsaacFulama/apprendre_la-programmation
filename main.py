from app.models.produit import Produit
from app.api.main_api import app


def main() -> None:
    produit = Produit(
        identifiant_produit=1,
        nom="Produit 1",
        description="Description du produit 1",
        prix=10.0,
        quantite=5,
    )
    print(f"Produit créé : {produit.nom} - {produit.prix} €")
    print("Pour démarrer l'API, exécutez : uvicorn app.api.main_api:app --reload")


if __name__ == "__main__":
    main()
