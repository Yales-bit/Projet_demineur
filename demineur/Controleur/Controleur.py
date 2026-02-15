import sys
from PySide6.QtWidgets import QApplication
from ..Modele.database import SessionLocal, initialiser_db
from ..Modele.Modele import SauvegardePartie, Etat, SauvegardeCase

# Gestion des imports circulaires ou contextuels pour la Grille
try:
    from .Grille import Grille
except ImportError:
    from Grille import Grille
    
# Gestion des imports pour la Vue (Interface Graphique)
try:
    from ..Vue.Vue import FenetreDemineur
except ImportError:
    from Vue.Vue import FenetreDemineur

class Controleur:
    """
    Le Contrôleur fait le pont entre le Modèle (Données/Base de données) 
    et la Vue (Interface PySide6). Il contient la logique métier.
    """
    def __init__(self):
        # Initialisation de la base de données et de la session SQLAlchemy
        initialiser_db()
        self.session = SessionLocal()
        
        # Gestion de l'état initial : on vérifie s'il existe une sauvegarde
        self.partie_id = None 
        self.grille = self.charger_partie_existante()
        
        # Si aucune sauvegarde "EN_COURS" n'est trouvée, on crée une nouvelle grille
        if self.grille is None:
            print("Nouvelle partie : Initialisation...")
            self.grille = Grille(n_mines=10, taille=10)
        else:
            print("Partie en cours chargée avec succès.")

        # Initialisation application graphique Qt
        self.app = QApplication(sys.argv)
        self.fenetre = FenetreDemineur(self)
        self.fenetre.show()

    def lancer(self):
        """Lance la boucle principale de l'application."""
        sys.exit(self.app.exec())

    def charger_partie_existante(self):
        """
        Cherche la dernière partie non terminée en base de données.
        Reconstruit l'objet Grille à partir des données SQL.
        """
        last_save = self.session.query(SauvegardePartie)\
            .filter(SauvegardePartie.statut_jeu == Etat.EN_COURS)\
            .order_by(SauvegardePartie.date_creation.desc())\
            .first()

        if not last_save:
            return None

        self.partie_id = last_save.id

        # Reconstruction de la grille avec les paramètres sauvegardés
        grille_chargee = Grille(n_mines=last_save.nb_mines_total, taille=last_save.nb_lignes)
        grille_chargee.premier_clic = False 
        
        # Restauration état de chaque cellule 
        for case_db in last_save.cases:
            cell = grille_chargee.grille[case_db.col_cellule][case_db.ligne_cellule]
            cell.est_mine = case_db.est_mine
            cell.est_decouverte = case_db.est_decouverte
            cell.est_drapeau = case_db.est_drapeau
            cell.nombre_mines_voisines = case_db.nombre_mines_voisines
            
        return grille_chargee
    
    def sauvegarder_etat_actuel(self):
        """
        Synchronise l'état actuel de la Grille Python avec la base de données SQLite.
        Met à jour la partie existante ou en crée une nouvelle au premier clic.
        """
        # 1. Récupérer ou Créer l'objet SauvegardePartie
        if self.partie_id:
            # Si la partie existe, on nettoie les anciennes cases pour éviter les doublons
            nouvelle_save = self.session.query(SauvegardePartie).get(self.partie_id)
            if nouvelle_save:
                self.session.query(SauvegardeCase).filter_by(id_partie=self.partie_id).delete()
                nouvelle_save.cases = []
        else:
            # Création entrée principale pour une nouvelle partie
            nouvelle_save = SauvegardePartie(
                nom_joueur="Joueur", 
                nb_lignes=self.grille.taille,
                nb_colonnes=self.grille.taille,
                nb_mines_total=self.grille.n_mines,
                statut_jeu=Etat.EN_COURS
            )
            self.session.add(nouvelle_save)
            self.session.flush() # Récupération de l'ID
            self.partie_id = nouvelle_save.id

        # 2. Parcourir la grille Python ( pour cahque cellule, un objet SQLAlchemy)
        for x in range(self.grille.taille):
            for y in range(self.grille.taille):
                c = self.grille.grille[x][y]
                
                case_db = SauvegardeCase(
                    col_cellule=x,
                    ligne_cellule=y,
                    est_mine=c.est_mine,
                    est_decouverte=c.est_decouverte,
                    est_drapeau=c.est_drapeau,
                    nombre_mines_voisines=c.nombre_mines_voisines
                )
                # Ajout de la case à la relation parent-enfant
                nouvelle_save.cases.append(case_db)

        # 3. Validation transaction SQL
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback() # Annulation en cas d'erreur 
            print(f"Erreur lors de la sauvegarde : {e}")

    def supprimer_partie(self):
        """Supprime la sauvegarde quand la partie est finie (Victoire ou Défaite)."""
        if self.partie_id:
            # Suppression des cases, ainsi que de la partie
            self.session.query(SauvegardeCase).filter_by(id_partie=self.partie_id).delete()
            partie = self.session.query(SauvegardePartie).get(self.partie_id)
            if partie:
                self.session.delete(partie)
            
            self.session.commit()
            self.partie_id = None
            print("Sauvegarde supprimée (Partie terminée).")

    # --- Méthodes de gestion des événements de la Vue ---

    def traiter_clic_gauche(self, ligne, colonne):
        """Action déclenchée par l'UI lors d'un clic gauche sur une case."""
        cellule = self.grille.grille[ligne][colonne]
        
        # Sécurité : on ne révèle pas une case déjà faite ou marquée
        if cellule.est_drapeau or cellule.est_decouverte:
            return 

        # Logique de révélation dans le modèle Grille
        resultat = self.grille.revele_case_clic(ligne, colonne)
        
        # Persistance de l'état après le coup
        self.sauvegarder_etat_actuel()
        self.fenetre.rafraichir_grille()

        if resultat == 0:
            # Cas d'une mine touchée
            self.supprimer_partie()
            self.fenetre.afficher_message_fin("BOOM ! Vous avez perdu.")
        
        # Vérification condition de victoire après chaque clic valide
        elif self.verifier_victoire():
            self.supprimer_partie()
            self.fenetre.afficher_message_fin("FELICITATIONS ! Vous avez gagné !")

    def traiter_clic_droit(self, ligne, colonne):
        """Action déclenchée par l'UI pour poser/enlever un drapeau."""
        cellule = self.grille.grille[ligne][colonne]
        
        if not cellule.est_decouverte:
            cellule.alterner_drapeau()
            self.sauvegarder_etat_actuel()
            self.fenetre.rafraichir_grille()

    def verifier_victoire(self):
        """
        Parcourt la grille pour vérifier s'il reste des cases saines à découvrir.
        Retourne True si le joueur a gagné.
        """
        for x in range(self.grille.taille):
            for y in range(self.grille.taille):
                cell = self.grille.grille[x][y]
                if not cell.est_mine and not cell.est_decouverte:
                    return False
        return True

def main():
    """Point d'entrée du script."""
    ctrl = Controleur()
    ctrl.lancer()

if __name__ == "__main__":
    main()