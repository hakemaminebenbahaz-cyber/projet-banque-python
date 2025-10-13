from compte import CompteBancaire

# Création d'un compte test
compte = CompteBancaire("Ross")

# Dépôt et retrait
compte.deposer(500)
compte.retirer(1000)

# Afficher le solde
print(f"Solde final de {compte.titulaire} : {compte.solde}")
