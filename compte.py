class CompteBancaire:
    def __init__(self, titulaire, solde=2000):
        self.titulaire = titulaire
        import random
        self.account_number = random.randint(1000000000, 9999999999)
        self.solde = solde
        self.historique = []
