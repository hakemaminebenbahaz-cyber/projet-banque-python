import tkinter as tk
from tkinter import messagebox
from user import UserManager 
from compte import CompteBancaire

class Application(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Banque - Connexion")
        self.geometry("400x300")
        self.configure(bg="#f0f0f0")

        self.show_login()


    def show_login(self):
        self.clear_window()
        tk.Label(self, text="Nom d'utilisateur:").pack(pady=5)
        self.entry_user = tk.Entry(self)
        self.entry_user.pack()

        tk.Label(self, text="Mot de passe:").pack(pady=5)
        self.entry_pass = tk.Entry(self, show="*")
        self.entry_pass.pack()

        tk.Button(self, text="Se connecter", command=self.login).pack(pady=20)


    def login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        manager = UserManager("data/comptes.json")
        compte = manager.verifier_login(username, password)

        if compte:
            self.compte_actuel = compte
            self.show_dashboard(username)
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")


    def show_dashboard(self, user):
        self.clear_window()
        tk.Label(self, text=f"Tableau de bord de {user}", font=("Arial", 14)).pack(pady=10)

        self.label_solde = tk.Label(self, text=f"Solde: {self.compte_actuel.solde} €", font=("Arial", 12))
        self.label_solde.pack(pady=10)

        tk.Button(self, text="Déposer", command=self.popup_deposer).pack(pady=5)
        tk.Button(self, text="Retirer", command=self.popup_retirer).pack(pady=5)
        tk.Button(self, text="Transférer", command=self.popup_transferer).pack(pady=5)
        tk.Button(self, text="Historique", command=self.popup_historique).pack(pady=5)
        tk.Button(self, text="Se déconnecter", command=self.show_login).pack(pady=10)


    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    
    def popup_deposer(self):
        self.popup_operation("deposer")

    def popup_retirer(self):
        self.popup_operation("retirer")

    def popup_operation(self, type_op):
        popup = tk.Toplevel(self)
        popup.title(f"{type_op.capitalize()} de l'argent")
        tk.Label(popup, text="Montant :").pack(pady=5)
        entry_montant = tk.Entry(popup)
        entry_montant.pack(pady=5)

        def valider():
            try:
                montant = float(entry_montant.get())
                if type_op == "deposer":
                    self.compte_actuel.deposer(montant)
                else:
                    self.compte_actuel.retirer(montant)
                self.label_solde.config(text=f"Solde: {self.compte_actuel.solde} €")
                messagebox.showinfo("Succès", "Opération réussie")
                popup.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "Montant invalide")

        tk.Button(popup, text="Valider", command=valider).pack(pady=10)



if __name__ == "__main__":
    app = Application()
    app.mainloop()
