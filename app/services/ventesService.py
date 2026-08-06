class ServiceVente:
    def __init__(self, depot_ventes):
        self.depot_ventes = depot_ventes

    def obtenir_toutes_les_ventes(self):
        return self.depot_ventes.get_all_ventes()

    def obtenir_vente_par_id(self, identifiant_vente):
        return self.depot_ventes.get_vente_by_id(identifiant_vente)

    def creer_vente(self, vente):
        return self.depot_ventes.create_vente(vente)

    def mettre_a_jour_vente(self, identifiant_vente, vente):
        return self.depot_ventes.update_vente(identifiant_vente, vente)

    def supprimer_vente(self, identifiant_vente):
        return self.depot_ventes.delete_vente(identifiant_vente)