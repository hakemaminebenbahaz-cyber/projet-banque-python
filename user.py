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

