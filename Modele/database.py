from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, SauvegardePartie, SauvegardeCase

# Définition de l'emplacement de la base de données
# Le fichier "demineur.db" sera créé à la racine de votre projet
DATABASE_URL = "sqlite:///demineur.db"

engine = create_engine(DATABASE_URL, echo=True)

#permer de créer des transactions pour sauvegarder/charger
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def initialiser_db():
    """
    Crée le fichier .db et toutes les tables définies dans models.py
    si elles n'existent pas encore.
    """
    print("Initialisation de la base de données...")
    Base.metadata.create_all(bind=engine)
    print("Base de données prête.")