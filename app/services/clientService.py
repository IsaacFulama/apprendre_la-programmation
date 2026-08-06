from app.models.client import Client


class ServiceClient:
    def __init__(self, depot_client):
        self.depot_client = depot_client

    def obtenir_tous_les_clients(self):
        return self.depot_client.get_all()

    def obtenir_client_par_id(self, identifiant_client):
        return self.depot_client.get_by_id(identifiant_client)

    def creer_client(self, client: Client):
        return self.depot_client.create(client)
