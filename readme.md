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
│
├── controllers/
│   ├── __pycache__/
│   ├── game_controller.py
│   └── main_controller.py
│
├── grids/
│   ├── grille_01.json
│   ├── grille_02.json
│   ├── (...)
│   └── grille_50.json
│
├── modele/
│   ├── __pycache__/
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
