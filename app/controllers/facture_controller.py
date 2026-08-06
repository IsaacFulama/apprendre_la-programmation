from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.repositories.facture_repository import DepotFacture
from app.services.factureService import ServiceFacture

router = APIRouter(prefix="/factures", tags=["Factures"])
service_facture = ServiceFacture(DepotFacture())


class FacturePayload(BaseModel):
    identifiant_client: int = Field(..., description="Identifiant du client")
    identifiant_fournisseur: int = Field(..., description="Identifiant du fournisseur")
    montant: float = Field(..., gt=0, description="Montant de la facture")
    date_facture: str = Field(..., description="Date de la facture")


class FactureResponse(BaseModel):
    identifiant_client: int
    identifiant_fournisseur: int
    montant: float
    date_facture: str


@router.get("/", response_model=List[FactureResponse], summary="Lister les factures")
def lister_factures():
    return service_facture.obtenir_toutes_les_factures()


@router.post("/", response_model=FactureResponse, summary="Créer une facture")
def creer_facture(payload: FacturePayload):
    return service_facture.creer_facture(
        payload.identifiant_client,
        payload.identifiant_fournisseur,
        payload.montant,
        payload.date_facture,
    )
