import tkinter as tk
from tkinter import messagebox
from user import UserManager 

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
        tk.Label(self, text=f"Bienvenue {user}", font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="Se déconnecter", command=self.show_login).pack(pady=10)


    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
            

if __name__ == "__main__":
    app = Application()
    app.mainloop()
