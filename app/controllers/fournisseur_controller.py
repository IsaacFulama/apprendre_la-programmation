from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/fournisseurs", tags=["Fournisseurs"])


class FournisseurPayload(BaseModel):
    nom: str = Field(..., description="Nom du fournisseur")
    email: str = Field(..., description="Email du fournisseur")
    telephone: str = Field(..., description="Téléphone du fournisseur")


class FournisseurResponse(BaseModel):
    id: int
    nom: str
    email: str
    telephone: str


@router.get("/", response_model=List[FournisseurResponse], summary="Lister les fournisseurs")
def lister_fournisseurs():
    return [
        FournisseurResponse(id=1, nom="Fournisseur A", email="contact@fournisseur-a.com", telephone="0123456789"),
    ]


@router.post("/", response_model=FournisseurResponse, summary="Créer un fournisseur")
def creer_fournisseur(payload: FournisseurPayload):
    return FournisseurResponse(id=2, nom=payload.nom, email=payload.email, telephone=payload.telephone)
