from dataclasses import dataclass


@dataclass
class Fournisseur:
    identifiant_fournisseur: int
    nom: str
    email: str
    telephone: str