from app.models.client import Client


class ServiceClient:
    def __init__(self):
        self.clients = []

    def ajouter_client(self, client: Client):
        self.clients.append(client)

    def obtenir_clients(self):
        return self.clients