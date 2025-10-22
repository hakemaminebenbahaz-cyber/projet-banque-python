class CompteBancaire:  
    # Définition d'une classe représentant un compte bancaire
    def __init__(self, titulaire, solde=2000):
        # Le constructeur initialise les attributs d'un compte
        self.titulaire = titulaire  # Nom du propriétaire du compte
        import random  # On importe random ici pour générer un numéro de compte aléatoire
        self.account_number = random.randint(1000000000, 9999999999)  # Numéro de compte à 10 chiffres
        self.solde = solde  # Solde initial (par défaut 2000)
        self.epargne = 0  # Montant mis de côté sur le compte épargne
        self.historique = []  # Liste qui contiendra toutes les opérations effectuées

   
    # MÉTHODE : Dépôt d'argent
   
    def deposer(self, montant):
        self.solde += montant  # On ajoute le montant au solde
        self.historique.append(f"Dépôt : +{montant}")  # On garde une trace dans l'historique

   
    # MÉTHODE : Retrait d'argent
  
    def retirer(self, montant):
        if montant <= self.solde:  # On vérifie que le solde est suffisant
            self.solde -= montant  # On soustrait le montant
            self.historique.append(f"Retrait : -{montant}")  # On ajoute à l'historique
        else:
            print(f"Solde insuffisant pour {self.titulaire} !")  # Message d’erreur si solde trop bas

    
    # MÉTHODE : Transfert entre deux comptes
    
    def transferer(self, autre_compte, montant):
        if montant <= self.solde:  # Vérifie que le compte a assez d'argent
            self.solde -= montant  # Débite le compte source
            autre_compte.solde += montant  # Crédite le compte destinataire
            # Historique pour les deux comptes :
            self.historique.append(f"Transfert : -{montant} vers {autre_compte.titulaire}")
            autre_compte.historique.append(f"Transfert : +{montant} de {self.titulaire}")
        else:
            print(f"Solde insuffisant pour {self.titulaire} !")

    
    # MÉTHODE : Épargner (mettre de côté)
    
    def epargner(self, montant):
        if montant <= self.solde:  # Vérifie si le montant est disponible
            self.solde -= montant  # On retire l'argent du solde principal
            self.epargne += montant  # On ajoute à la réserve épargne
            self.historique.append(f"Epargne : -{montant}")  # On note l'opération
        else:
            print(f"Solde insuffisant pour {self.titulaire} !")

    
    # MÉTHODE : Afficher l’historique des opérations
    
    def afficher_historique(self):
        print(f"Historique de {self.titulaire} :")  # Titre
        for operation in self.historique:  # On parcourt la liste des opérations
            print(operation)  # Et on les affiche une par une

    
    # MÉTHODE : Afficher les infos du compte
    
    def afficher(self):
        print(f"{self.titulaire}, {self.account_number}, {self.solde}")
        # Affiche le nom du titulaire, le numéro du compte, et le solde actuel
