from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/categories", tags=["Catégories"])


class CategoriePayload(BaseModel):
    nom: str = Field(..., description="Nom de la catégorie")
    description: str = Field(..., description="Description de la catégorie")


class CategorieResponse(BaseModel):
    id: int
    nom: str
    description: str


@router.get("/", response_model=List[CategorieResponse], summary="Lister les catégories")
def lister_categories():
    return [
        CategorieResponse(id=1, nom="Électronique", description="Appareils électroniques"),
        CategorieResponse(id=2, nom="Maison", description="Produits de maison"),
    ]


@router.post("/", response_model=CategorieResponse, summary="Créer une catégorie")
def creer_categorie(payload: CategoriePayload):
    return CategorieResponse(id=3, nom=payload.nom, description=payload.description)
