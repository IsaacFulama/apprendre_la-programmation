class DepotClient:
    def __init__(self):
        self.clients = []

    def get_all(self):
        return self.clients

    def get_by_id(self, identifiant_client):
        return next((client for client in self.clients if client.identifiant_client == identifiant_client), None)

    def create(self, client):
        self.clients.append(client)
        return client
