class ServiceFacture:
    def __init__(self, depot_facture):
        self.depot_facture = depot_facture

    def creer_facture(self, identifiant_client, identifiant_fournisseur, montant, date_facture):
        return self.depot_facture.creer_facture(identifiant_client, identifiant_fournisseur, montant, date_facture)

    def obtenir_facture(self, identifiant_facture):
        return self.depot_facture.obtenir_facture(identifiant_facture)

    def mettre_a_jour_facture(self, identifiant_facture, **kwargs):
        return self.depot_facture.mettre_a_jour_facture(identifiant_facture, **kwargs)

    def supprimer_facture(self, identifiant_facture):
        return self.depot_facture.supprimer_facture(identifiant_facture)