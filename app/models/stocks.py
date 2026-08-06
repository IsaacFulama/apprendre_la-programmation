from dataclasses import dataclass


@dataclass
class Stocks:
    identifiant_stock: int
    identifiant_produit: int
    quantite: int