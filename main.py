
from gui import Application

if __name__ == "__main__":
    try:
        app = Application()
        app.mainloop()
    except Exception as e:
        print("Une erreur est survenue lors de l’exécution de l’application :", e)
