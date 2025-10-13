import json

def charger_comptes():
    with open("data/comptes.json", "r") as f:
        return json.load(f)

def sauvegarder_comptes(comptes):
    with open("data/comptes.json", "w") as f:
        json.dump(comptes, f, indent=4)
