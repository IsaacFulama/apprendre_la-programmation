class BaseDeDonnees:
    def __init__(self):
        self.connexion = None

    def connecter(self):
        self.connexion = "Connexion établie"
        return self.connexion

    def deconnecter(self):
        self.connexion = None
        return "Connexion fermée"
