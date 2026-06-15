# NÉONAURE

## Participants du projet

* **Trilla Selim** — `Strill4`
* **Ymamou Younais** — `MisterFaulty`
* **Deléglise Charly** — `charlydeleglise`

---

## Architecture du projet

```
NEONAURE-SAE/
│
├── __pycache__/
│   ├── interfacev1.cpython-314.pyc
│   ├── main.cpython-314.pyc
│   ├── neonaure.cpython-314.pyc
│   └── test.cpython-314.pyc
│
├── controllers/
│   ├── __pycache__/
│   ├── game_controller.py
│   └── main_controller.py
│
├── grids/
│   ├── grids_alea/
│   │   ├── grille1.json
│   │   ├── grille2.json
│   │   ├── grille3.json
│   │   ├── grille4.json
│   │   ├── grille5.json
│   │   └── grille6.json
│   └── grids_cpg/
│
├── modele/
│   ├── __pycache__/
│   │   ├── __init__.cpython-313.pyc
│   │   ├── __init__.cpython-314.pyc
│   │   ├── a.cpython-314.pyc
│   │   ├── Case.cpython-313.pyc
│   │   ├── Case.cpython-314.pyc
│   │   ├── GridFiller.cpython-314.pyc
│   │   ├── Grille.cpython-313.pyc
│   │   ├── Grille.cpython-314.pyc
│   │   ├── LevelGenerator.cpython-313.pyc
│   │   ├── LevelGenerator.cpython-314.pyc
│   │   ├── Motif.cpython-313.pyc
│   │   ├── Motif.cpython-314.pyc
│   │   ├── RandomGenerator.cpython-314.pyc
│   │   ├── Solver.cpython-313.pyc
│   │   ├── Solver.cpython-314.pyc
│   │   ├── Validator.cpython-313.pyc
│   │   └── Validator.cpython-314.pyc
│   ├── Case.py
│   ├── GridFiller.py
│   ├── Grille.py
│   ├── LevelGenerator.py
│   ├── Motif.py
│   ├── RandomGenerator.py
│   ├── Solver.py
│   └── Validator.py
│
├── views/
│   ├── __pycache__/
│   │   ├── custom_widgets.cpython-313.pyc
│   │   ├── custom_widgets.cpython-314.pyc
│   │   ├── game_view.cpython-313.pyc
│   │   ├── game_view.cpython-314.pyc
│   │   ├── start_page.cpython-313.pyc
│   │   └── start_page.cpython-314.pyc
│   ├── custom_widgets.py
│   ├── game_view.py
│   └── start_page.py
│
├── main.py
├── maquette.png
└── readme.md
```

---

## Démarrage

Pour lancer le jeu :

1. Télécharger le dossier **`neonaure-sae`**
2. Ouvrir un terminal
3. Exécuter la commande suivante :
```bash
c:/chemin_vers_le_dossier/neonaure-sae/main.py
```

---

## Remarques

* Projet structuré selon une architecture **MVC (Model - View - Controller)**
* Génération de grilles et logique de jeu séparées de l’interface
* Interface graphique personnalisée dans le dossier `views/`

---
