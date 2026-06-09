import json
import matplotlib.pyplot as plt
import numpy as np
import traceback
import os

def charger_grille(dossier, nom_fichier):
    # Construit le chemin complet vers le fichier
    chemin_complet = os.path.join(dossier, nom_fichier)
    
    if not os.path.exists(chemin_complet):
        raise FileNotFoundError(f"Le fichier est introuvable ici : {chemin_complet}")
        
    with open(chemin_complet, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def afficher_grille(data, taille=8):
    # Initialisation de la matrice 8x8 avec des zéros
    grille_visuelle = np.zeros((taille, taille))
    
    # Remplissage de la matrice à partir des données JSON
    for motif, cellules in data.items():
        if not isinstance(cellules, list):
            continue
            
        for cellule in cellules:
            try:
                # Conversion sécurisée des coordonnées et de la valeur
                x, y, valeur = map(int, cellule)
                
                # Inversion des axes pour correspondre à la structure (ligne, colonne)
                if 0 <= y < taille and 0 <= x < taille:
                    grille_visuelle[y, x] = valeur
            except (ValueError, TypeError):
                continue

    # Configuration de l'affichage
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(grille_visuelle, cmap='Blues', origin='upper', alpha=0.3)

    # Ajout des chiffres sur la grille
    for i in range(taille):
        for j in range(taille):
            val = grille_visuelle[i, j]
            if val != 0:
                ax.text(j, i, int(val), ha='center', va='center', fontsize=16, fontweight='bold')

    # Dessin des lignes de la grille
    ax.set_xticks(np.arange(-.5, taille, 1), minor=True)
    ax.set_yticks(np.arange(-.5, taille, 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
    ax.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    
    plt.title("Visualisation de la grille de Sudoku")
    plt.show()

if __name__ == "__main__":
    try:
        
        dossier_cible = "." 
        nom_du_fichier = "grille_sudoku.json"
        
        data = charger_grille(dossier_cible, nom_du_fichier)
        afficher_grille(data)
    except Exception:
        print("Une erreur est survenue lors du traitement :")
        traceback.print_exc()