# Projet Demineur

Bienvenue dans ce projet de Demineur en Python.
Il s'agit d'une implementation complete du jeu classique avec une architecture MVC (Modele-Vue-Controleur) et une interface graphique moderne basee sur PySide6.

## Pre-requis

- Python 3.9 ou superieur.
- pip (gestionnaire de paquets Python).

## Installation

1. Cloner le projet (ou telecharger les fichiers) :
   ```bash
   git clone <URL_DU_REPO>
   cd Projet_demineur
   ```

2. Creer un environnement virtuel (recommande) :
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Mac/Linux
   # ou
   venv\Scripts\activate     # Sur Windows
   ```

3. Installer les dependances :
   ```bash
   pip install .[test]
   # ou pour developper en editant le code :
   pip install -e .[test]
   ```
   
   Cela installera automatiquemnt les dependances decrites dans `pyproject.toml`.

## Lancer le Jeu

Le projet est structure comme un package Python. Pour lancer le jeu, executez la commande suivante a la racine du projet :

```bash
python3 -m demineur
```

## Tests Unitaires

Le projet inclut une suite de tests unitaires pour garantir le bon fonctionnement de la logique et de la persistance des donnees.

Pour lancer les tests :
```bash
pytest Tests
```

## Structure du Projet

- demineur/ : Le code source du jeu.
  - Controleur/ : Logique de jeu et gestion des evenements.
  - Modele/ : Gestion des donnees et base de donnees SQLite.
  - Vue/ : Interface graphique avec PySide6.
- Tests/ : Tests unitaires (avec Pytest).
- demineur.db : Fichier de base de donnees (genere automatiquement).

## Fonctionnalites

- Interface Graphique : Grille interactive, drapeaux, revelation en cascade.
- Sauvegarde Automatique : Votre partie est sauvegardée à chaque coup. Si vous fermez le jeu, vous reprendrez exactement où vous étiez.
- Victoire/Defaite : Detection de fin de partie avec messages.
