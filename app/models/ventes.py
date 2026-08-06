from dataclasses import dataclass


@dataclass
class Ventes:
    identifiant_vente: int
    identifiant_produit: int
    identifiant_client: int
    quantite: int
    date_vente: str