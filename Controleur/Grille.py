import random
from Cellule import Cellule


class Grille:
    def __init__(self, n_mines:int, taille:int):
        
        self.n_mines = n_mines
        self.taille = taille
        self.premier_clic = True
        self.grille = [[Cellule() for _ in range(taille)] for _ in range(taille)]

        emplacements = random.sample(range(taille * taille), n_mines)

        

    def generer_mines(self, l_exclue:int, c_exclue:int):
        indices_exclus = []
        for i in range(l_exclue - 1, l_exclue + 2):
            for j in range(c_exclue - 1, c_exclue + 2):
                if 0 <= i < self.taille and 0 <= j < self.taille:
                    indices_exclus.append(i * self.taille + j)
        
        possibilites = [i for i in range(self.taille * self.taille) if i not in indices_exclus]
        emplacements = random.sample(possibilites, self.n_mines)

        for pos in emplacements:
            ligne, col = pos // self.taille, pos % self.taille
            self.grille[ligne][col].definir_comme_mine()

            for i in range(ligne - 1, ligne + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < self.taille and 0 <= j < self.taille:
                        if not (i == ligne and j == col):
                            self.grille[i][j].incremente_nombre()

    def revele_case_clic(self, ligne:int, col: int):

        if self.premier_clic:
            self.generer_mines(ligne, col)
            self.premier_clic = False

        self.grille[ligne][col].decouvrir()
        if(self.grille[ligne][col].est_mine):
            self.revele_toutes_les_mines()
            return 0
        else:
            if(self.grille[ligne][col].nombre_mines_voisines==0):
                self.revele_case_reaction_en_chaine(ligne,col)
            return 1


    def revele_toutes_les_mines(self):
        for ligne in range(len(self.grille)):
            for col in range(len(self.grille[ligne])):
                cellule = self.grille[ligne][col]
            
                if cellule.est_mine:
                    cellule.decouvrir()

    def revele_case_reaction_en_chaine(self, ligne:int, col: int):
        for l in range(ligne - 1, ligne + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= l < self.taille and 0 <= c < self.taille:
                        if not (l == ligne and c == col):
                            if not self.grille[l][c].est_decouverte:
                                if not(self.grille[l][c].est_mine):
                                    self.grille[l][c].decouvrir()
                                    if(self.grille[l][c].nombre_mines_voisines==0):
                                        self.revele_case_reaction_en_chaine(l,c)


    


        

    
        

