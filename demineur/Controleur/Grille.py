import random

# Gestion de l'import de la classe Cellule selon le contexte d'exécution
try:
    from .Cellule import Cellule
except ImportError:
    from Cellule import Cellule


class Grille:
    """
    Gère la logique de la grille de jeu : génération des mines, 
    calcul des voisinages et propagation des révélations (réaction en chaîne).
    """
    def __init__(self, n_mines:int, taille:int):
        # Initialisation des paramètres de base
        self.n_mines = n_mines
        self.taille = taille
        self.premier_clic = True # Flag pour garantir que le premier clic n'est jamais une mine
        
        # Création de la matrice de Cellules (Lignes x Colonnes)
        self.grille = [[Cellule(ligne_cellule,col_cellule) for col_cellule in range(taille)] for ligne_cellule in range(taille)]

        # Note : emplacements ici n'est pas utilisé dans l'init car on génère au premier clic
        emplacements = random.sample(range(taille * taille), n_mines)

    def generer_mines(self, l_exclue:int, c_exclue:int):
        """
        Place les mines aléatoirement sur la grille en évitant la zone du premier clic 
        et met à jour les compteurs de mines voisines pour chaque cellule.
        """
        indices_exclus = []
        # On définit une zone de sécurité (3x3) autour du premier clic
        for i in range(l_exclue - 1, l_exclue + 2):
            for j in range(c_exclue - 1, c_exclue + 2):
                if 0 <= i < self.taille and 0 <= j < self.taille:
                    indices_exclus.append(i * self.taille + j)
        
        # On tire les mines parmi les cases qui ne sont pas dans la zone exclue
        possibilites = [i for i in range(self.taille * self.taille) if i not in indices_exclus]
        emplacements = random.sample(possibilites, self.n_mines)

        for pos in emplacements:
            ligne, col = pos // self.taille, pos % self.taille
            self.grille[ligne][col].definir_comme_mine()

            # Mise à jour des nombres des voisins (8 directions) autour de la nouvelle mine
            for i in range(ligne - 1, ligne + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < self.taille and 0 <= j < self.taille:
                        if not (i == ligne and j == col):
                            self.grille[i][j].incremente_nombre()

    def revele_case_clic(self, ligne:int, col: int):
        """
        Gère l'action de cliquer sur une case. 
        Retourne 0 en cas de défaite (mine), 1 sinon.
        """
        # Si c'est le premier coup, on génère les mines maintenant pour éviter la zone du clic
        if self.premier_clic:
            self.generer_mines(ligne, col)
            self.premier_clic = False

        self.grille[ligne][col].decouvrir()
        
        if(self.grille[ligne][col].est_mine):
            # Le joueur a touché une mine
            self.revele_toutes_les_mines()
            return 0
        else:
            # Si la case est vide (0 mine autour), on propage la découverte
            if(self.grille[ligne][col].nombre_mines_voisines==0):
                self.revele_case_reaction_en_chaine(ligne,col)
            return 1

    def revele_toutes_les_mines(self):
        """Révèle toutes les mines de la grille (appelé lors de la défaite)."""
        for ligne in range(len(self.grille)):
            for col in range(len(self.grille[ligne])):
                cellule = self.grille[ligne][col]
            
                if cellule.est_mine:
                    cellule.decouvrir()

    def revele_case_reaction_en_chaine(self, ligne:int, col: int):
        """
        Algorithme récursif pour découvrir automatiquement les cases vides adjacentes.
        """
        for l in range(ligne - 1, ligne + 2):
                for c in range(col - 1, col + 2):
                    # Vérification des limites de la grille
                    if 0 <= l < self.taille and 0 <= c < self.taille:
                        if not (l == ligne and c == col):
                            # Si la case voisine n'est pas encore découverte et n'est pas une mine
                            if not self.grille[l][c].est_decouverte:
                                if not(self.grille[l][c].est_mine):
                                    self.grille[l][c].decouvrir()
                                    # Si le voisin est aussi vide, on continue la récursion
                                    if(self.grille[l][c].nombre_mines_voisines==0):
                                        self.revele_case_reaction_en_chaine(l,c)