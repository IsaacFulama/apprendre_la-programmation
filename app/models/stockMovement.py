from dataclasses import dataclass


@dataclass
class MouvementStock:
    identifiant_mouvement: int
    identifiant_stock: int
    quantite: int
    date_mouvement: str