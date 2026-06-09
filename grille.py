import json
def generer_grille_vide(taille=8):
    grille = []
    for x in range(taille):
        for y in range(taille):
            grille.append([x, y, 0])
    return {"grille_sudoku": grille}
donnees = generer_grille_vide(8)
with open("grille_auto.json", "w") as f:
    json.dump(donnees, f, indent=4)
nom_fichier = "grille_sudoku.json"
with open(nom_fichier, 'w', encoding='utf-8') as fichier_json:
    print(f" La grille a été exportée dans le fichier : {nom_fichier}")

    
