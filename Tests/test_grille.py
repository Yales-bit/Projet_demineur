import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Controleur.Grille import Grille
from Controleur.Cellule import Cellule, etat

@pytest.fixture
def grille_test():
    """Fixture qui fournit une grille fraîche pour chaque test."""
    return Grille(n_mines=10, taille=10)

def test_initialisation(grille_test):
    """Vérifie que la grille est bien initialisée."""
    assert len(grille_test.grille) == 10
    assert len(grille_test.grille[0]) == 10
    assert grille_test.premier_clic is True
    assert grille_test.n_mines == 10

def test_generation_mines(grille_test):
    """Vérifie que les mines sont générées correctement après le premier clic."""
    grille_test.revele_case_clic(5, 5)
    
    compteur_mines = 0
    for x in range(10):
        for y in range(10):
            if grille_test.grille[x][y].est_mine:
                compteur_mines += 1
    
    assert compteur_mines == 10
    assert grille_test.premier_clic is False
    
    # Vérifie que la case cliquée initialement n'est PAS une mine (règle du premier clic)
    assert not grille_test.grille[5][5].est_mine

def test_drapeau(grille_test):
    """Vérifie le placement et retrait de drapeau."""
    cellule = grille_test.grille[0][0]
    assert not cellule.est_drapeau
    
    cellule.alterner_drapeau()
    assert cellule.est_drapeau
    
    cellule.alterner_drapeau()
    assert not cellule.est_drapeau

def test_decouverte_cellule(grille_test):
    """Vérifie qu'une cellule se découvre."""
    cellule = grille_test.grille[2][2]
    assert not cellule.est_decouverte
    
    cellule.decouvrir()
    assert cellule.est_decouverte
