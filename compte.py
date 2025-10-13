class CompteBancaire:
    def __init__(self, titulaire, solde=2000):
        self.titulaire = titulaire
        import random
        self.account_number = random.randint(1000000000, 9999999999)
        self.solde = solde
        self.historique = []


    def deposer(self, montant):
        self.solde += montant
        self.historique.append(f"Dépôt : +{montant}")

    def retirer(self, montant):
        if montant <= self.solde:
            self.solde -= montant
            self.historique.append(f"Retrait : -{montant}")
        else:
            print(f"Solde insuffisant pour {self.titulaire} !")
    def transferer(self, autre_compte, montant):
        if montant <= self.solde:
            self.solde -= montant
            autre_compte.solde += montant
            self.historique.append(f"Transfert : -{montant} vers {autre_compte.titulaire}")
            autre_compte.historique.append(f"Transfert : +{montant} de {self.titulaire}")
        else:
            print(f"Solde insuffisant pour {self.titulaire} !")

    def epargner(self, montant):
        if montant <= self.solde:
            self.solde -= montant
            self.epargne += montant
            self.historique.append(f"Epargne : -{montant}")
        else:
            print(f"Solde insuffisant pour {self.titulaire} !")

    def afficher_historique(self):
        print(f"Historique de {self.titulaire} :")
        for operation in self.historique:
            print(operation)
