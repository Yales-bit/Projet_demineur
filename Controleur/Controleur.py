from Modele.database import SessionLocal, initialiser_db
from Modele.model import SauvegardePartie, Etat, SauvegardeCase
from Controleur.Cellule import Cellule
from Controleur.Grille import Grille

Taille = 8    

class Controleur:
    def __init__(self):
        initialiser_db()
        self.session = SessionLocal()
        
        # On initialise la variable à None par défaut
        self.partie_id = None 
        self.grille = self.charger_partie_existante()
        
        if self.grille is None:
            print("Nouvelle partie : Initialisation...")
            self.grille = Grille(n_mines=10, taille=10)
        else:
            print("Partie en cours chargée avec succès.")

    def charger_partie_existante(self):
        last_save = self.session.query(SauvegardePartie)\
            .filter(SauvegardePartie.statut_jeu == Etat.EN_COURS)\
            .order_by(SauvegardePartie.date_creation.desc())\
            .first()

        if not last_save:
            return None

        grille_chargee = Grille(n_mines=last_save.nb_mines_total, taille=last_save.nb_lignes)
        grille_chargee.premier_clic = False 
        
        for case_db in last_save.cases:
            cell = grille_chargee.grille[case_db.col_cellule][case_db.ligne_cellule]
            cell.est_mine = case_db.est_mine
            cell.est_decouverte = case_db.est_decouverte
            cell.est_drapeau = case_db.est_drapeau
            cell.nombre_mines_voisines = case_db.nombre_mines_voisines
            
        return grille_chargee
    
    def sauvegarder_etat_actuel(self):
        # 1. Récupérer ou Créer l'objet SauvegardePartie
        if self.partie_id:
            # On récupère la partie existante dans la session
            nouvelle_save = self.session.query(SauvegardePartie).get(self.partie_id)
            if nouvelle_save:
                # On vide les anciennes cases pour cette partie (Nettoyage)
                self.session.query(SauvegardeCase).filter_by(id_partie=self.partie_id).delete()
                # On s'assure que la liste des cases liée à l'objet est vide
                nouvelle_save.cases = []
        else:
            # C'est le tout premier clic : on crée la ligne 'parties'
            nouvelle_save = SauvegardePartie(
                nom_joueur="Joueur",  # Tu pourras demander le nom plus tard
                nb_lignes=self.grille.taille,
                nb_colonnes=self.grille.taille,
                nb_mines_total=self.grille.n_mines,
                statut_jeu=Etat.EN_COURS
            )
            self.session.add(nouvelle_save)
            self.session.flush()  # Génère l'ID immédiatement sans fermer la transaction
            self.partie_id = nouvelle_save.id

        # 2. Parcourir la grille et ajouter les cases
        for x in range(self.grille.taille):
            for y in range(self.grille.taille):
                c = self.grille.grille[x][y]
                
                # Création de l'objet case lié à la partie
                case_db = SauvegardeCase(
                    col_cellule=x,
                    ligne_cellule=y,
                    est_mine=c.est_mine,
                    est_decouverte=c.est_decouverte,
                    est_drapeau=c.est_drapeau,
                    nombre_mines_voisines=c.nombre_mines_voisines
                )
                # On l'ajoute à la relation "cases" de notre partie
                nouvelle_save.cases.append(case_db)

        # 3. On valide les changements dans la base de données
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Erreur lors de la sauvegarde : {e}")

    def supprimer_partie(self):
        if self.partie_id:
            # On supprime les cases d'abord (intégrité référentielle)
            self.session.query(SauvegardeCase).filter_by(id_partie=self.partie_id).delete()
            # On supprime la partie elle-même
            partie = self.session.query(SauvegardePartie).get(self.partie_id)
            if partie:
                self.session.delete(partie)
            
            self.session.commit()
            self.partie_id = None
            print("Sauvegarde supprimée (Partie terminée).")

def main():
    ctrl = Controleur()
    grille = ctrl.grille 

    while True:
        try:
            print("\nGrille actuelle :")
            for ligne_index, ligne_obj in enumerate(grille.grille):
                print([("D" if c.est_drapeau else ("?" if not c.est_decouverte else (c.nombre_mines_voisines))) for c in ligne_obj])
            
            entree = input("\nAction (Ligne Colonne Action) ex: '5 2 C' pour casser ou '5 2 D' pour drapeau : ").split()
            
            if len(entree) < 3:
                print("Format invalide. Utilisez : Ligne Colonne Action (C ou D)")
                continue

            l = int(entree[0])
            c = int(entree[1])
            action = entree[2].upper()

            if action == 'D':
                grille.grille[l][c].est_drapeau = not grille.grille[l][c].est_drapeau
                print(f"Drapeau {'placé' if grille.grille[l][c].est_drapeau else 'retiré'} en ({l}, {c})")
                ctrl.sauvegarder_etat_actuel()
            
            elif action == 'C':
                if grille.grille[l][c].est_drapeau:
                    print("Impossible de casser une case avec un drapeau ! Retirez-le d'abord.")
                    continue
                    
                resultat = grille.revele_case_clic(l, c)
                
                if resultat == 0:
                    print("\nBOOM ! Partie terminée.")
                    ctrl.supprimer_partie()
                    break
                else:
                    ctrl.sauvegarder_etat_actuel()
            else:
                print("Action inconnue. Utilisez 'C' pour casser ou 'D' pour drapeau.")

        except (ValueError, IndexError):
            print("Entrée invalide. Vérifiez les coordonnées et le format.")
        
if __name__ == "__main__":
    main()