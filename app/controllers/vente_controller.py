from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/ventes", tags=["Ventes"])


class VentePayload(BaseModel):
    identifiant_produit: int = Field(..., description="Identifiant du produit")
    quantite: int = Field(..., gt=0, description="Quantité vendue")
    montant: float = Field(..., gt=0, description="Montant de la vente")


class VenteResponse(BaseModel):
    identifiant_vente: int
    identifiant_produit: int
    quantite: int
    montant: float


@router.get("/", response_model=List[VenteResponse], summary="Lister les ventes")
def lister_ventes():
    return [VenteResponse(identifiant_vente=1, identifiant_produit=1, quantite=2, montant=20.0)]


@router.post("/", response_model=VenteResponse, summary="Créer une vente")
def creer_vente(payload: VentePayload):
    return VenteResponse(
        identifiant_vente=2,
        identifiant_produit=payload.identifiant_produit,
        quantite=payload.quantite,
        montant=payload.montant,
    )
