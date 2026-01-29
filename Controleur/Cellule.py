from enum import Enum

class etat(Enum):
    DRAPEAU = "drapeau"
    CACHE = "cache"
    DECOUVERT = "decouvert"


class Cellule:

    def __init__(self, est_mine=False):
        self.est_mine = est_mine
        self.est_decouverte = False
        self.est_drapeau = False
        self.voisin = None
        self.nombre = 0

    def __repr__(self):
        if self.est_mine:
            return "X"
        else:
            return str(self.nombre)
        
    #méthodes pour contrôleur
    def set_nombre(self, nombre):
        self.nombre = nombre

    def incremente_nombre(self):
        self.nombre += 1

    def definir_comme_mine(self):
        self.est_mine = True



    #méthodes pour interface
    def decouvrir(self):
        if not self.est_drapeau:
            self.est_decouverte = True


    def alterner_drapeau(self):
        if not self.est_decouverte
            self.est_drapeau = not self.est_drapeau

    
