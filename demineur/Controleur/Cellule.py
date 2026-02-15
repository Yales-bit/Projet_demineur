from enum import Enum

# Définition des états possibles pour une cellule (utilisé pour la logique globale)
class etat(Enum):
    DRAPEAU = "drapeau"
    CACHE = "cache"
    DECOUVERT = "decouvert"


class Cellule:
    """
    Représente une case unique de la grille du démineur.
    Stocke ses coordonnées, son contenu (mine ou non) et son état d'affichage.
    """

    def __init__(self, ligne_cellule:int, col_cellule:int, est_mine=False):
        # Coordonnées de la cellule dans la grille
        self.ligne_cellule = ligne_cellule
        self.col_cellule = col_cellule
        
        # Attributs de contenu
        self.est_mine = est_mine
        self.nombre_mines_voisines = 0
        
        # Attributs d'état (affichage)
        self.est_decouverte = False
        self.est_drapeau = False

    def __repr__(self):
        if not self.est_decouverte:
            return "☐" # Case non révélée
        else:
            if self.est_mine:
                return "X" # Mine révélée
            else:
                return str(self.nombre_mines_voisines) # Chiffre révélé
        
    # --- Méthodes utilisées par le contrôleur pour la mise en place du jeu ---
    
    def set_nombre(self, nombre):
        """Définit directement le nombre de mines aux alentours."""
        self.nombre_mines_voisines = nombre

    def incremente_nombre(self):
        """Augmente de 1 le compteur de mines voisines (utile lors du placement des mines)."""
        self.nombre_mines_voisines += 1

    def definir_comme_mine(self):
        """Transforme cette cellule en mine."""
        self.est_mine = True

    # --- Méthodes d'interaction (Interface utilisateur / Logique de jeu) ---
    
    def decouvrir(self):
        """
        Révèle la cellule. 
        Le changement ne se fait que si aucun drapeau n'est posé dessus.
        """
        if not self.est_drapeau:
            self.est_decouverte = True

    def alterner_drapeau(self):
        """
        Pose ou retire un drapeau.
        Action possible uniquement si la cellule est encore cachée.
        """
        if not self.est_decouverte:
            self.est_drapeau = not self.est_drapeau