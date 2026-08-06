class DepotFacture:
    def __init__(self):
        self.factures = []

    def creer_facture(self, identifiant_client, identifiant_fournisseur, montant, date_facture):
        facture = {
            "identifiant_client": identifiant_client,
            "identifiant_fournisseur": identifiant_fournisseur,
            "montant": montant,
            "date_facture": date_facture,
        }
        self.factures.append(facture)
        return facture

    def obtenir_facture(self, identifiant_facture):
        return self.factures[identifiant_facture] if identifiant_facture < len(self.factures) else None

    def mettre_a_jour_facture(self, identifiant_facture, **kwargs):
        if identifiant_facture < len(self.factures):
            self.factures[identifiant_facture].update(kwargs)
            return self.factures[identifiant_facture]
        return None

    def supprimer_facture(self, identifiant_facture):
        if identifiant_facture < len(self.factures):
            del self.factures[identifiant_facture]
            return True
        return False
