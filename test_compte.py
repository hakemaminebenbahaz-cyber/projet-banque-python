from compte import CompteBancaire

ross = CompteBancaire("Ross")
rachel = CompteBancaire("Rachel")

ross.deposer(500)
ross.transferer(rachel, 300)
ross.epargner(200)

ross.afficher()
rachel.afficher()
