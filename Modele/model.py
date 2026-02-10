from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, ForeignKey, Boolean
from datetime import datetime
from enum import Enum

class Etat(Enum):
    EN_COURS = "EN_COURS"
    GAGNEE = "GAGNEE"
    PERDUE = "PERDUE"


# La classe de base dont tous nos modèles vont hériter
class Base(DeclarativeBase):
    pass


class SauvegardePartie(Base):
    """
    Représente une partie sauvegardée dans la table 'parties'.
    """
    __tablename__ = 'parties'

    # --- Colonnes d'identification ---
    # La Clé Primaire : L'ID unique de la sauvegarde
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Nom optionnel (ex: "Partie de Pierre") et date automatique
    nom_joueur = Column(String, nullable=True, default="Joueur")
    date_creation = Column(DateTime, default=datetime.now)

    # --- Données globales du jeu ---
    # Le chrono arrêté au moment de la sauvegarde (en secondes)
    temps_ecoule = Column(Integer, default=0)
    
    # L'état global : "en_cours", "victoire", "defaite"
    statut_jeu = Column(Etat, default="EN_COURS")

    # Dimensions (Nécessaires pour reconstruire la grille vide avant de la remplir)
    nb_lignes = Column(Integer, default=10, nullable=False)
    nb_colonnes = Column(Integer, default=10, nullable=False)
    nb_mines_total = Column(Integer, nullable=False)

    # --- La Relation (Lien avec les cases) ---
    # C'est ici que se fait le lien avec la table des cases.
    # 'cascade="all, delete-orphan"' est très important : 
    # cela signifie que si on supprime une Partie de la DB, 
    # toutes les Cases associées seront supprimées automatiquement.
    cases = relationship(
        "SauvegardeCase", 
        back_populates="partie", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Partie(id={self.id}, date={self.date_creation}, statut={self.statut_jeu})>"


class SauvegardeCase(Base):
    """
    Représente une case sauvegardée dans la table 'cases'.
    """
    __tablename__ = 'cases'

    # La Clé d'identification : L'ID unique de la sauvegarde
    id = Column(Integer, primary_key=True, autoincrement=True)
    # La clé de partie : L'ID qui la lie a sa partie
    id_partie = Column(Integer, ForeignKey('parties.id'), nullable=False)

    x_coord = Column(Integer, nullable = False)
    y_coord = Column(Integer, nullable = False)
    est_mine = Column(Boolean, nullable = False)
    est_decouverte = Column(Boolean, nullable = False)
    est_drapeau = Column(Boolean, nullable = False)
    voisin = Column(Integer, nullable = False)

    # Relation inverse : Permet d'accéder à la partie depuis la case (ex: ma_case.partie)
    partie = relationship("SauvegardePartie", back_populates="cases")

    def __repr__(self):
        return f"<Case(id={self.id}, x={self.x_coord}, y={self.y_coord}, est_mine={self.est_mine})>"
    
