import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt, QSize, Signal

class CaseGraphique(QPushButton):
    """
    Représente une case dans l'interface graphique.
    Émet des signaux pour les clics gauche et droit.
    """
    # Signaux pour notifier le contrôleur
    clic_gauche = Signal(int, int)
    clic_droit = Signal(int, int)

    def __init__(self, ligne, colonne):
        super().__init__()
        self.ligne = ligne
        self.colonne = colonne
        self.setFixedSize(QSize(40, 40))
        self.setStyleSheet("""
            QPushButton {
                background-color: #d7dce1;
                border: 1px solid #9aa5b1;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c5ccd3;
            }
        """)

    def mousePressEvent(self, event):
        """Gestion des clics souris."""
        if event.button() == Qt.LeftButton:
            self.clic_gauche.emit(self.ligne, self.colonne)
        elif event.button() == Qt.RightButton:
            self.clic_droit.emit(self.ligne, self.colonne)
        super().mousePressEvent(event) # Important pour l'effet visuel du clic

    def mettre_a_jour(self, etat_texte, style):
        """Met à jour l'apparence de la case."""
        self.setText(etat_texte)
        self.setStyleSheet(style)


class FenetreDemineur(QWidget):
    """
    Fenêtre principale du jeu Démineur.
    """
    def __init__(self, controleur):
        super().__init__()
        self.controleur = controleur
        self.nb_lignes = controleur.grille.taille
        self.nb_colonnes = controleur.grille.taille
        self.cases_graphiques = [] # Matrice des widgets boutons

        self.setWindowTitle("Démineur")
        # Taille ajustée dynamiquement serait mieux, mais fixe pour l'instant comme demandé "plus simple"
        # self.setFixedSize(45 * self.nb_colonnes, 45 * self.nb_lignes + 50)

        self.layout_principal = QVBoxLayout()
        self.setLayout(self.layout_principal)

        self.initialiser_grille()
        
        # Premier affichage
        self.rafraichir_grille()

    def initialiser_grille(self):
        """Crée la grille de boutons."""
        self.layout_grille = QGridLayout()
        self.layout_grille.setSpacing(1)

        for l in range(self.nb_lignes):
            ligne_cases = []
            for c in range(self.nb_colonnes):
                bouton = CaseGraphique(l, c)
                # Connexion des signaux aux méthodes du contrôleur
                bouton.clic_gauche.connect(self.controleur.traiter_clic_gauche)
                bouton.clic_droit.connect(self.controleur.traiter_clic_droit)
                
                self.layout_grille.addWidget(bouton, l, c)
                ligne_cases.append(bouton)
            self.cases_graphiques.append(ligne_cases)

        self.layout_principal.addLayout(self.layout_grille)

    def rafraichir_grille(self):
        """Met à jour l'affichage de toute la grille en fonction du modèle."""
        grille_modele = self.controleur.grille.grille

        for l in range(self.nb_lignes):
            for c in range(self.nb_colonnes):
                cellule = grille_modele[l][c]
                bouton = self.cases_graphiques[l][c]

                texte = ""
                texte = ""
                # Initialisation des propriétés CSS
                props_css = """
                    border: 1px solid #9aa5b1;
                    font-weight: bold;
                    font-size: 14px;
                """
                hover_css = ""

                if cellule.est_decouverte:
                    if cellule.est_mine:
                        texte = "💣"
                        props_css += "background-color: #e74c3c; color: black;" # Rouge pour mine
                    else:
                        nb = cellule.nombre_mines_voisines
                        if nb > 0:
                            texte = str(nb)
                            # Couleurs classiques du démineur
                            couleurs = {1: "blue", 2: "green", 3: "red", 4: "darkblue", 5: "brown", 6: "cyan", 7: "black", 8: "gray"}
                            couleur_texte = couleurs.get(nb, "black")
                            props_css += f"background-color: #ecf0f1; color: {couleur_texte}; border: 1px solid #bdc3c7;"
                        else:
                            props_css += "background-color: #ecf0f1; border: 1px solid #bdc3c7;" # Gris clair pour vide
                
                elif cellule.est_drapeau:
                    texte = "🚩"
                    props_css += "background-color: #d7dce1; color: red;"
                
                else:
                    # Case cachée normale
                    props_css += "background-color: #d7dce1;"
                    hover_css = "QPushButton:hover { background-color: #c5ccd3; }"

                # On assemble le tout
                # Attention : Les propriétés principales doivent être dans le bloc QPushButton { ... }
                style_final = f"QPushButton {{ {props_css} }} {hover_css}"

                bouton.mettre_a_jour(texte, style_final)

    def afficher_message_fin(self, message):
        """Affiche une popup de fin de partie."""
        msg = QMessageBox()
        msg.setWindowTitle("Fin de partie")
        msg.setText(message)
        msg.exec()
        self.close()
