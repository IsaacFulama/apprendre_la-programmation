from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.models.client import Client
from app.repositories.client_repository import DepotClient
from app.services.clientService import ServiceClient

router = APIRouter(prefix="/clients", tags=["Clients"])
service_client = ServiceClient(DepotClient())


class ClientPayload(BaseModel):
    nom: str = Field(..., description="Nom du client")
    email: str = Field(..., description="Email du client")
    telephone: str = Field(..., description="Téléphone du client")


class ClientResponse(BaseModel):
    id: int
    nom: str
    email: str
    telephone: str


def convertir_en_modele(client: Client) -> ClientResponse:
    return ClientResponse(
        id=client.identifiant_client,
        nom=client.nom,
        email=client.email,
        telephone=client.telephone,
    )


@router.get("/", response_model=List[ClientResponse], summary="Lister les clients")
def lister_clients():
    clients = service_client.obtenir_tous_les_clients()
    return [convertir_en_modele(client) for client in clients]


@router.post("/", response_model=ClientResponse, summary="Créer un client")
def creer_client(payload: ClientPayload):
    nouveau_client = Client(
        identifiant_client=len(service_client.obtenir_tous_les_clients()) + 1,
        nom=payload.nom,
        email=payload.email,
        telephone=payload.telephone,
    )
    service_client.creer_client(nouveau_client)
    return convertir_en_modele(nouveau_client)
