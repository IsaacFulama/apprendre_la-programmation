from app.models.produit import Produit


class ServiceProduit:
    def __init__(self, depot_produit):
        self.depot_produit = depot_produit

    def obtenir_tous_les_produits(self):
        return self.depot_produit.get_all()

    def obtenir_produit_par_id(self, identifiant_produit):
        return self.depot_produit.get_by_id(identifiant_produit)

    def creer_produit(self, produit: Produit):
        return self.depot_produit.create(produit)

    def mettre_a_jour_produit(self, identifiant_produit, produit: Produit):
        return self.depot_produit.update(identifiant_produit, produit)

    def supprimer_produit(self, identifiant_produit):
        return self.depot_produit.delete(identifiant_produit)