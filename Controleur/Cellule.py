

class etat(enum.Enum):
    DRAPEAU = "drapeau"
    CACHE = "cache"
    DECOUVERT = "decouvert"


class Cellule:

    def __init__(self, est_mine=False):
        self.est_mine = est_mine
        self.est_decouverte = False
        self.est_drapeau = False
        self.voisin = None

    def set_nombre(self, nombre):
        self.nombre = nombre

    def decouvrir(self):
        if not self.est_drapeau:
            self.est_decouverte = True

    def reveler(self):
        pass

    def alterner_drapeau(self):
        pass

    def definir_comme_mine(self):
        pass

    def to_dict(self):
        pass
