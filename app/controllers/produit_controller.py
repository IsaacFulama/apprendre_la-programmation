from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from app.models.produit import Produit
from app.repositories.produit_repository import DepotProduit
from app.services.produitService import ServiceProduit

router = APIRouter(prefix="/produits", tags=["Produits"])

# Initialisation différée : l'import du routeur ne doit pas créer une base locale.
_service_produit: ServiceProduit | None = None


def get_service_produit() -> ServiceProduit:
    global _service_produit
    if _service_produit is None:
        _service_produit = ServiceProduit(DepotProduit())
    return _service_produit


class ProduitPayload(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nom: str = Field(..., min_length=1, max_length=120, description="Nom du produit")
    description: str = Field(..., min_length=1, max_length=2000, description="Description du produit")
    prix: float = Field(..., gt=0, allow_inf_nan=False, description="Prix strictement positif et fini")
    quantite: int = Field(..., ge=0, description="Quantité disponible, zéro autorisé")


class ProduitResponse(BaseModel):
    id: int
    nom: str
    description: str
    prix: float
    quantite: int


def convertir_en_modele(produit: Produit) -> ProduitResponse:
    return ProduitResponse(
        id=produit.identifiant_produit,
        nom=produit.nom,
        description=produit.description,
        prix=produit.prix,
        quantite=produit.quantite,
    )


@router.get("/", response_model=List[ProduitResponse], summary="Lister les produits")
def lister_produits(service: ServiceProduit = Depends(get_service_produit)):
    produits = service.obtenir_tous_les_produits()
    return [convertir_en_modele(produit) for produit in produits]


@router.get("/{identifiant_produit}", response_model=ProduitResponse, summary="Obtenir un produit")
def obtenir_produit(
    identifiant_produit: int,
    service: ServiceProduit = Depends(get_service_produit),
):
    produit = service.obtenir_produit_par_id(identifiant_produit)
    if produit is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return convertir_en_modele(produit)


@router.post("/", response_model=ProduitResponse, status_code=201, summary="Créer un produit")
def creer_produit(
    payload: ProduitPayload,
    service: ServiceProduit = Depends(get_service_produit),
):
    # SQLite attribue l'identifiant afin d'éviter les collisions après une suppression.
    nouveau_produit = Produit(
        identifiant_produit=0,
        nom=payload.nom,
        description=payload.description,
        prix=payload.prix,
        quantite=payload.quantite,
    )
    produit_cree = service.creer_produit(nouveau_produit)
    if produit_cree is None:
        raise HTTPException(status_code=500, detail="Le produit n'a pas pu être enregistré")
    return convertir_en_modele(produit_cree)


@router.put("/{identifiant_produit}", response_model=ProduitResponse, summary="Mettre à jour un produit")
def mettre_a_jour_produit(
    identifiant_produit: int,
    payload: ProduitPayload,
    service: ServiceProduit = Depends(get_service_produit),
):
    produit_modifie = Produit(
        identifiant_produit=identifiant_produit,
        nom=payload.nom,
        description=payload.description,
        prix=payload.prix,
        quantite=payload.quantite,
    )
    resultat = service.mettre_a_jour_produit(identifiant_produit, produit_modifie)
    if resultat is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return convertir_en_modele(resultat)


@router.delete("/{identifiant_produit}", summary="Supprimer un produit")
def supprimer_produit(
    identifiant_produit: int,
    service: ServiceProduit = Depends(get_service_produit),
):
    supprime = service.supprimer_produit(identifiant_produit)
    if not supprime:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return {"message": "Produit supprimé avec succès"}
