from dataclasses import dataclass


@dataclass
class Facture:
    identifiant_facture: int
    identifiant_client: int
    identifiant_fournisseur: int
    montant: float
    date_facture: str