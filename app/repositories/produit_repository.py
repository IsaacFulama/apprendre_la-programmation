import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from app.models.produit import Produit


class DepotProduit:
    def __init__(self, db_path=None):
        base_dir = Path(__file__).resolve().parents[2]
        self.db_path = Path(db_path) if db_path else base_dir / "produits.db"
        self._initialiser_schema()

    @contextmanager
    def _get_connection(self) -> Iterator[sqlite3.Connection]:
        connexion = sqlite3.connect(self.db_path)
        connexion.row_factory = sqlite3.Row
        try:
            # Le context manager sqlite gère commit/rollback ; le finally ferme
            # explicitement la connexion pour éviter une fuite de ressources.
            with connexion:
                yield connexion
        finally:
            connexion.close()

    def _initialiser_schema(self):
        with self._get_connection() as connexion:
            connexion.execute(
                """
                CREATE TABLE IF NOT EXISTS produits (
                    identifiant_produit INTEGER PRIMARY KEY,
                    nom TEXT NOT NULL,
                    description TEXT NOT NULL,
                    prix REAL NOT NULL,
                    quantite INTEGER NOT NULL
                )
                """
            )
            connexion.commit()

            # Si une ancienne base contient un schéma incompatible, on le répare.
            colonnes = [ligne[1] for ligne in connexion.execute("PRAGMA table_info(produits)").fetchall()]
            if "identifiant_produit" not in colonnes:
                connexion.execute("ALTER TABLE produits RENAME COLUMN id TO identifiant_produit")
                connexion.commit()

    def get_all(self):
        with self._get_connection() as connexion:
            lignes = connexion.execute(
                "SELECT identifiant_produit, nom, description, prix, quantite FROM produits ORDER BY identifiant_produit"
            ).fetchall()
        return [self._convertir_en_modele(ligne) for ligne in lignes]

    def get_by_id(self, identifiant_produit):
        with self._get_connection() as connexion:
            ligne = connexion.execute(
                "SELECT identifiant_produit, nom, description, prix, quantite FROM produits WHERE identifiant_produit = ?",
                (identifiant_produit,),
            ).fetchone()
        return self._convertir_en_modele(ligne) if ligne else None

    def create(self, produit):
        # Laisser SQLite attribuer la clé primaire évite les collisions liées à len(...) + 1.
        with self._get_connection() as connexion:
            curseur = connexion.execute(
                "INSERT INTO produits (nom, description, prix, quantite) VALUES (?, ?, ?, ?)",
                (produit.nom, produit.description, produit.prix, produit.quantite),
            )
            connexion.commit()
            identifiant = curseur.lastrowid
        return self.get_by_id(identifiant)

    def update(self, identifiant_produit, produit):
        with self._get_connection() as connexion:
            connexion.execute(
                "UPDATE produits SET nom = ?, description = ?, prix = ?, quantite = ? WHERE identifiant_produit = ?",
                (
                    produit.nom,
                    produit.description,
                    produit.prix,
                    produit.quantite,
                    identifiant_produit,
                ),
            )
            connexion.commit()
        return self.get_by_id(identifiant_produit)

    def delete(self, identifiant_produit):
        with self._get_connection() as connexion:
            curseur = connexion.execute(
                "DELETE FROM produits WHERE identifiant_produit = ?",
                (identifiant_produit,),
            )
            connexion.commit()
        return curseur.rowcount > 0

    def _convertir_en_modele(self, ligne):
        if ligne is None:
            return None
        return Produit(
            identifiant_produit=ligne["identifiant_produit"],
            nom=ligne["nom"],
            description=ligne["description"],
            prix=ligne["prix"],
            quantite=ligne["quantite"],
        )
