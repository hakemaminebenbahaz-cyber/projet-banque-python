from compte import CompteBancaire
import json

def charger_comptes():
    with open("data/comptes.json", "r") as f:
        return json.load(f)

def sauvegarder_comptes(comptes):
    with open("data/comptes.json", "w") as f:
        json.dump(comptes, f, indent=4)
def verifier_login(username, password, comptes):
    if username in comptes and comptes[username]["password"] == password:
        print(f"Connexion réussie pour {username} - Compte n° {comptes[username]['numero_compte']}")
        return True
    return False

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