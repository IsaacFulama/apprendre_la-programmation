from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/stocks", tags=["Stocks"])


class StockPayload(BaseModel):
    identifiant_produit: int = Field(..., description="Identifiant du produit")
    quantite: int = Field(..., ge=0, description="Quantité en stock")


class StockResponse(BaseModel):
    identifiant_stock: int
    identifiant_produit: int
    quantite: int


@router.get("/", response_model=List[StockResponse], summary="Lister les stocks")
def lister_stocks():
    return [StockResponse(identifiant_stock=1, identifiant_produit=1, quantite=10)]


@router.post("/", response_model=StockResponse, summary="Créer un stock")
def creer_stock(payload: StockPayload):
    return StockResponse(identifiant_stock=2, identifiant_produit=payload.identifiant_produit, quantite=payload.quantite)
