import tkinter as tk
from tkinter import messagebox
from user import (
    verifier_login, 
    charger_comptes, 
    charger_compte_utilisateur, 
    sauvegarder_compte_utilisateur
)
from compte import CompteBancaire

# ---------- Thème / couleurs de l'interface ----------
BG_COLOR = "#f5f6fa"
PRIMARY_COLOR = "#4a90e2"
SECONDARY_COLOR = "#ffffff"
TEXT_COLOR = "#2f3640"
BUTTON_HOVER_COLOR = "#357ab8"

# ---------- Bouton avec effet hover (UI) ----------
class HoverButton(tk.Button):
    """Bouton personnalisé qui change de couleur au survol."""
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["bg"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["bg"] = BUTTON_HOVER_COLOR

    def on_leave(self, e):
        self["bg"] = self.defaultBackground

# ---------- Application principale ----------
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        # Configuration fenêtre principale
        self.title("EPSI Bank")
        self.geometry("500x400")
        self.configure(bg=BG_COLOR)
        self.minsize(500, 400)

        # Affiche l'écran de connexion au démarrage
        self.show_login()

    # --- Écran de connexion ---
    def show_login(self):
        """Affichage des champs de connexion (username / password) et bouton."""
        self.clear_window()
        tk.Label(self, text="Nom d'utilisateur", bg=BG_COLOR, fg=TEXT_COLOR, font=("Helvetica", 16)).pack(pady=10)
        self.entry_user = tk.Entry(self, font=("Helvetica", 16))
        self.entry_user.pack(pady=5, ipadx=10, ipady=5)

        tk.Label(self, text="Mot de passe", bg=BG_COLOR, fg=TEXT_COLOR, font=("Helvetica", 16)).pack(pady=10)
        self.entry_pass = tk.Entry(self, show="*", font=("Helvetica", 16))
        self.entry_pass.pack(pady=5, ipadx=10, ipady=5)

        login_btn = HoverButton(self, text="Se connecter", command=self.login,
                                bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, font=("Helvetica", 16), relief="flat")
        login_btn.pack(pady=30, ipadx=20, ipady=10)

    # --- Authentification ---
    def login(self):
        """
        Vérifie les identifiants via les fonctions user.py.
        Charge le compte utilisateur en mémoire si ok.
        """
        username = self.entry_user.get()
        password = self.entry_pass.get()
        comptes = charger_comptes()
        if verifier_login(username, password, comptes):
            # charge l'objet CompteBancaire pour l'utilisateur connecté
            self.compte_actuel = charger_compte_utilisateur(username)
            self.show_dashboard(username)
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")

    # --- Tableau de bord ---
    def show_dashboard(self, user):
        """Affiche solde et boutons d'actions principales (déposer/retirer/transfer/...)."""
        self.clear_window()
        tk.Label(self, text=f"EPSI Bank - {user}", bg=BG_COLOR, fg=TEXT_COLOR, font=("Helvetica", 18, "bold")).pack(pady=15)
        self.label_solde = tk.Label(self, text=f"{self.compte_actuel.solde} €", bg=BG_COLOR, fg=PRIMARY_COLOR, font=("Helvetica", 24))
        self.label_solde.pack(pady=20)

        buttons_frame = tk.Frame(self, bg=BG_COLOR)
        buttons_frame.pack(pady=10, expand=True, fill="both")

        # Liste des boutons et leurs callbacks
        btn_specs = [
            ("💰 Déposer", self.popup_deposer),
            ("💸 Retirer", self.popup_retirer),
            ("💳 Épargner", self.popup_epargner),
            ("🔄 Transférer", self.popup_transferer),
            ("📜 Historique", self.popup_historique),
            ("🔓 Se déconnecter", self.show_login)
        ]

        for text, cmd in btn_specs:
            btn = HoverButton(buttons_frame, text=text, command=cmd,
                              bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, font=("Helvetica", 16), relief="flat")
            btn.pack(pady=8, ipadx=10, ipady=8, fill="x", padx=50)

    # --- Utilitaire ---
    def clear_window(self):
        """Supprime tous les widgets pour recharger un nouvel écran."""
        for widget in self.winfo_children():
            widget.destroy()

    # --- Dépôt / Retrait (fenêtre générique) ---
    def popup_operation(self, type_op):
        """
        Fenêtre réutilisable pour déposer ou retirer:
        - met à jour le solde en mémoire
        - sauvegarde le compte via sauvegarder_compte_utilisateur
        """
        popup = tk.Toplevel(self)
        popup.configure(bg=BG_COLOR)
        popup.geometry("450x220")
        popup.title(type_op.capitalize())

        tk.Label(popup, text=f"Montant à {type_op}", bg=BG_COLOR, fg=TEXT_COLOR, font=("Helvetica", 16)).pack(pady=15)
        entry_montant = tk.Entry(popup, font=("Helvetica", 16), bd=2, relief="groove")
        entry_montant.pack(pady=5, fill="x", padx=50, ipady=8)

        def valider():
            try:
                montant = float(entry_montant.get())
                if type_op == "deposer":
                    self.compte_actuel.deposer(montant)
                elif type_op == "retirer":
                    self.compte_actuel.retirer(montant)

                # mise à jour UI et persistance du compte
                self.label_solde.config(text=f"{self.compte_actuel.solde} €")
                sauvegarder_compte_utilisateur(self.compte_actuel)
                messagebox.showinfo("Succès", f"{type_op.capitalize()} effectué")
                popup.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "Montant invalide")

        val_btn = HoverButton(popup, text="Valider", command=valider,
                              bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, font=("Helvetica", 16), relief="flat")
        val_btn.pack(pady=25, ipadx=20, ipady=10, fill="x", padx=50)

    def popup_deposer(self):
        self.popup_operation("deposer")

    def popup_retirer(self):
        self.popup_operation("retirer")

    # --- Épargner (fonction dédiée) ---
    def popup_epargner(self):
        """
        Permet de déplacer une partie du solde vers l'épargne (méthode epargner du compte).
        Sauvegarde le compte après modification.
        """
        popup = tk.Toplevel(self)
        popup.configure(bg=BG_COLOR)
        popup.geometry("450x220")
        popup.title("Épargner")

        tk.Label(popup, text="Montant à épargner", bg=BG_COLOR, fg=TEXT_COLOR, font=("Helvetica", 16)).pack(pady=15)
        entry_montant = tk.Entry(popup, font=("Helvetica", 16), bd=2, relief="groove")
        entry_montant.pack(pady=5, fill="x", padx=50, ipady=8)

        def valider():
            try:
                montant = float(entry_montant.get())
                self.compte_actuel.epargner(montant)
                self.label_solde.config(text=f"{self.compte_actuel.solde} €")
                sauvegarder_compte_utilisateur(self.compte_actuel)
                messagebox.showinfo("Succès", f"{montant} € mis de côté")
                popup.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "Montant invalide")

        val_btn = HoverButton(popup, text="Valider", command=valider,
                              bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, font=("Helvetica", 16), relief="flat")
        val_btn.pack(pady=25, ipadx=20, ipady=10, fill="x", padx=50)

    # --- Transfert vers un autre utilisateur ---
    def popup_transferer(self):
        """
        Demande destinataire + montant, charge le compte destinataire,
        effectue le transfert et sauvegarde les deux comptes.
        """
        popup = tk.Toplevel(self)
        popup.configure(bg=BG_COLOR)
        popup.geometry("450x250")
        popup.title("Transférer")

        tk.Label(popup, text="Destinataire", bg=BG_COLOR, fg=TEXT_COLOR, font=("Helvetica", 16)).pack(pady=10)
        entry_dest = tk.Entry(popup, font=("Helvetica", 16))
        entry_dest.pack(pady=5, fill="x", padx=50, ipady=8)

        tk.Label(popup, text="Montant", bg=BG_COLOR, fg=TEXT_COLOR, font=("Helvetica", 16)).pack(pady=10)
        entry_montant = tk.Entry(popup, font=("Helvetica", 16))
        entry_montant.pack(pady=5, fill="x", padx=50, ipady=8)

        def valider():
            try:
                montant = float(entry_montant.get())
                dest_nom = entry_dest.get()
                # charge l'objet CompteBancaire du destinataire
                dest_compte = charger_compte_utilisateur(dest_nom)
                if dest_compte:
                    self.compte_actuel.transferer(dest_compte, montant)
                    # mise à jour UI et persistance des deux comptes
                    self.label_solde.config(text=f"{self.compte_actuel.solde} €")
                    sauvegarder_compte_utilisateur(self.compte_actuel)
                    sauvegarder_compte_utilisateur(dest_compte)
                    messagebox.showinfo("Succès", "Transfert effectué")
                    popup.destroy()
                else:
                    messagebox.showerror("Erreur", "Destinataire introuvable")
            except ValueError:
                messagebox.showerror("Erreur", "Montant invalide")

        val_btn = HoverButton(popup, text="Valider", command=valider,
                              bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, font=("Helvetica", 16), relief="flat")
        val_btn.pack(pady=20, ipadx=20, ipady=10, fill="x", padx=50)

    # --- Historique des transactions ---
    def popup_historique(self):
        """Affiche l'historique enregistré dans l'objet compte."""
        popup = tk.Toplevel(self)
        popup.configure(bg=BG_COLOR)
        popup.geometry("500x400")
        popup.title("Historique")
        text = tk.Text(popup, width=60, height=20, font=("Helvetica", 14))
        text.pack(padx=10, pady=10, fill="both", expand=True)
        for ligne in self.compte_actuel.historique:
            text.insert(tk.END, ligne + "\n")
        text.config(state="disabled")

# --- Lancement de l'application ---
if __name__ == "__main__":
    app = Application()
    app.mainloop()
