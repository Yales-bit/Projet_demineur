import random
from Cellule import Cellule
from Grille import Grille

Taille = 8    


def main():
    grille = Grille(10,Taille)
    for i in range(Taille):
        print(grille.grille[i])

    while 1:
        ligne = int(input())
        colonne = int(input())
        grille.revele_case_clic(ligne,colonne)
        for i in range(Taille):
            print(grille.grille[i])
        
if __name__ == "__main__":
    main()