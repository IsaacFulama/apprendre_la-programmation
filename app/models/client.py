from dataclasses import dataclass


@dataclass
class Client:
    identifiant_client: int
    nom: str
    email: str
    telephone: str