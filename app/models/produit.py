from dataclasses import dataclass


@dataclass
class Produit:
    identifiant_produit: int
    nom: str
    description: str
    prix: float
    quantite: int