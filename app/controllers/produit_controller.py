# Importation des types nécessaires pour les annotations.
from typing import List

# Importation de FastAPI et des exceptions HTTP.
from fastapi import APIRouter, HTTPException

# Importation des outils de validation de données avec Pydantic.
from pydantic import BaseModel, Field

# Importation du modèle de domaine Produit.
from app.models.produit import Produit

# Importation du dépôt et du service pour la logique des produits.
from app.repositories.produit_repository import DepotProduit
from app.services.produitService import ServiceProduit

# Création du routeur pour toutes les routes liées aux produits.
router = APIRouter(prefix="/produits", tags=["Produits"])

# Instanciation du service avec un dépôt en mémoire.
service_produit = ServiceProduit(DepotProduit())


# Schéma demandé pour créer ou modifier un produit.
class ProduitPayload(BaseModel):
    # Le nom du produit est obligatoire.
    nom: str = Field(..., description="Nom du produit")
    # La description est obligatoire.
    description: str = Field(..., description="Description du produit")
    # Le prix doit être strictement positif.
    prix: float = Field(..., gt=0, description="Prix du produit")
    # La quantité doit être positive ou nulle.
    quantite: int = Field(..., ge=0, description="Quantité disponible")


# Schéma de réponse envoyé par l'API.
class ProduitResponse(BaseModel):
    # Identifiant du produit.
    id: int
    # Nom du produit.
    nom: str
    # Description du produit.
    description: str
    # Prix du produit.
    prix: float
    # Quantité disponible.
    quantite: int


# Fonction utilitaire pour convertir un objet métier en réponse API.
def convertir_en_modele(produit: Produit) -> ProduitResponse:
    # On transforme l'objet Produit du modèle métier vers le format de réponse.
    return ProduitResponse(
        id=produit.identifiant_produit,
        nom=produit.nom,
        description=produit.description,
        prix=produit.prix,
        quantite=produit.quantite,
    )


# Route pour lister tous les produits.
@router.get("/", response_model=List[ProduitResponse], summary="Lister les produits")
def lister_produits():
    # On récupère tous les produits via le service.
    produits = service_produit.obtenir_tous_les_produits()
    # On convertit chaque produit en réponse API.
    return [convertir_en_modele(produit) for produit in produits]


# Route pour récupérer un produit par son identifiant.
@router.get("/{identifiant_produit}", response_model=ProduitResponse, summary="Obtenir un produit")
def obtenir_produit(identifiant_produit: int):
    # On recherche le produit demandé.
    produit = service_produit.obtenir_produit_par_id(identifiant_produit)
    # Si le produit n'existe pas, on lève une erreur 404.
    if produit is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    # On retourne le produit converti.
    return convertir_en_modele(produit)


# Route pour créer un nouveau produit.
@router.post("/", response_model=ProduitResponse, summary="Créer un produit")
def creer_produit(payload: ProduitPayload):
    # On crée un objet Produit métier à partir des données reçues.
    nouveau_produit = Produit(
        identifiant_produit=len(service_produit.obtenir_tous_les_produits()) + 1,
        nom=payload.nom,
        description=payload.description,
        prix=payload.prix,
        quantite=payload.quantite,
    )
    # On enregistre le produit via le service.
    service_produit.creer_produit(nouveau_produit)
    # On retourne le produit créé.
    return convertir_en_modele(nouveau_produit)


# Route pour modifier un produit existant.
@router.put("/{identifiant_produit}", response_model=ProduitResponse, summary="Mettre à jour un produit")
def mettre_a_jour_produit(identifiant_produit: int, payload: ProduitPayload):
    # On crée une version mise à jour du produit.
    produit_modifie = Produit(
        identifiant_produit=identifiant_produit,
        nom=payload.nom,
        description=payload.description,
        prix=payload.prix,
        quantite=payload.quantite,
    )
    # On demande la mise à jour au service.
    resultat = service_produit.mettre_a_jour_produit(identifiant_produit, produit_modifie)
    # Si le produit n'existe pas, on signale une erreur 404.
    if resultat is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    # On retourne le produit mis à jour.
    return convertir_en_modele(produit_modifie)


# Route pour supprimer un produit.
@router.delete("/{identifiant_produit}", summary="Supprimer un produit")
def supprimer_produit(identifiant_produit: int):
    # On demande la suppression au service.
    service_produit.supprimer_produit(identifiant_produit)
    # On retourne un message de confirmation.
    return {"message": "Produit supprimé avec succès"}
