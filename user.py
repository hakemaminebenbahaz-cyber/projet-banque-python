from compte import CompteBancaire
import json

# Charge tous les comptes depuis le fichier JSON
def charger_comptes():
    with open("data/comptes.json", "r") as f:
        return json.load(f)

# Sauvegarde tous les comptes dans le fichier JSON
def sauvegarder_comptes(comptes):
    with open("data/comptes.json", "w") as f:
        json.dump(comptes, f, indent=4)

# Vérifie si le nom d'utilisateur et mot de passe sont corrects
def verifier_login(username, password, comptes):
    if username in comptes and comptes[username]["password"] == password:
        print(f"Connexion réussie pour {username} - Compte n° {comptes[username]['numero_compte']}")
        return True
    return False

# Charge les données d'un utilisateur spécifique et crée l'objet CompteBancaire
def charger_compte_utilisateur(username):
    comptes = charger_comptes()
    if username in comptes:
        data = comptes[username]
        compte = CompteBancaire(titulaire=username, solde=data["solde"])
        compte.epargne = data["epargne"]
        compte.historique = data["historique"]
        return compte
    else:
        print("Utilisateur non trouvé.")
        return None
        
# Sauvegarde les modifications d'un compte utilisateur
def sauvegarder_compte_utilisateur(compte):
    comptes = charger_comptes()
    comptes[compte.titulaire] = {
        "password": comptes[compte.titulaire]["password"],
        "numero_compte": comptes[compte.titulaire]["numero_compte"],
        "solde": compte.solde,
        "epargne": compte.epargne,
        "historique": compte.historique
    }
    sauvegarder_comptes(comptes)
