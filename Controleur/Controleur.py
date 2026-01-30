import random
from Cellule import Cellule
Taille = 8

def creer_grille(n_mines: int, taille = 10):
    """
    Crée une grille de 10x10, place les mines de façon aléatoire
    et calcule le nombre de mines adjacentes pour chaque cellule.
    """
    
    
    # Utilisation de list comprehension pour une initialisation propre (PEP 8)
    grille = [[Cellule() for _ in range(taille)] for _ in range(taille)]

    # Sélection de positions uniques sans répétition
    emplacements = random.sample(range(taille * taille), n_mines)

    for pos in emplacements:
        ligne, col = pos // taille, pos % taille
        grille[ligne][col].definir_comme_mine()

        # Parcours des 8 cellules adjacentes (carré 3x3 autour de la mine)
        for i in range(ligne - 1, ligne + 2):
            for j in range(col - 1, col + 2):
                # Vérification des limites de la grille
                if 0 <= i < taille and 0 <= j < taille:
                    # On n'incrémente pas la mine elle-même
                    if not (i == ligne and j == col):
                        grille[i][j].incremente_nombre()

    return grille
    


def main():
    k =creer_grille(20,Taille)
    for i in range(Taille):
        print(k[i])
        

if __name__ == "__main__":
    main()