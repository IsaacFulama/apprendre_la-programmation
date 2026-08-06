from dataclasses import dataclass


@dataclass
class Categorie:
    identifiant_categorie: int
    nom: str
    description: str