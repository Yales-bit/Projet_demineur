import sys
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ajout du dossier parent au path pour les imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Modele.Modele import Base, SauvegardePartie, SauvegardeCase, Etat

@pytest.fixture
def session_test():
    """Fixture pour la base de données en mémoire."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_creation_partie(session_test):
    """Vérifie qu'on peut créer et sauvegarder une partie."""
    partie = SauvegardePartie(
        nom_joueur="Testeur",
        nb_lignes=10,
        nb_colonnes=10,
        nb_mines_total=10,
        statut_jeu=Etat.EN_COURS
    )
    session_test.add(partie)
    session_test.commit()

    partie_recuperee = session_test.query(SauvegardePartie).first()
    assert partie_recuperee is not None
    assert partie_recuperee.nom_joueur == "Testeur"
    assert partie_recuperee.statut_jeu == Etat.EN_COURS

def test_ajout_cases(session_test):
    """Vérifie la relation entre Partie et Cases."""
    partie = SauvegardePartie(nb_mines_total=5)
    session_test.add(partie)
    session_test.commit()

    case1 = SauvegardeCase(
        col_cellule=0, ligne_cellule=0,
        est_mine=False, est_decouverte=True,
        est_drapeau=False, nombre_mines_voisines=1
    )
    partie.cases.append(case1)
    session_test.commit()

    partie_recuperee = session_test.query(SauvegardePartie).first()
    assert len(partie_recuperee.cases) == 1
    assert partie_recuperee.cases[0].nombre_mines_voisines == 1

def test_suppression_cascade(session_test):
    """Vérifie que supprimer une partie supprime ses cases."""
    partie = SauvegardePartie(nb_mines_total=5)
    case1 = SauvegardeCase(
        col_cellule=0, ligne_cellule=0,
        est_mine=True, est_decouverte=False,
        est_drapeau=False, nombre_mines_voisines=0
    )
    partie.cases.append(case1)
    session_test.add(partie)
    session_test.commit()

    partie_id = partie.id
    
    session_test.delete(partie)
    session_test.commit()

    partie_check = session_test.query(SauvegardePartie).filter_by(id=partie_id).first()
    case_check = session_test.query(SauvegardeCase).filter_by(id_partie=partie_id).first()
    
    assert partie_check is None
    assert case_check is None
