#Creation de la classe Grille du jeu Neonaure.
import json
from PIL import Image

class Grille:
    def __init__(self, taille=9):
        self.taille = taille
        self.donnees = self.generer_grille_vide()

    def generer_grille_vide(self):
        grille = []
        for x in range(self.taille):#boucle pour la ligne 
            for y in range(self.taille):#boucle pour la cologne 
                grille.append([x, y, 0])
        return {"grille_sudoku": grille}

    def charger_image(self):
        chemin_image = "Exemples de grille-20260609/grille1.png" #chemin relatif du fichier ou hardcoder 
        #gere l'ouverture du fichier et l'affichage du fichier 
        try:
            img = Image.open(chemin_image)
            img.show()
            print(f"Format: {img.format}, Taille: {img.size}, Mode: {img.mode}")# optionele donne des info sur l'image 
            #gestion des erreur envoi  un message d'erreru si il trouve pas le fichier ou si une erreur est ariver 
        except FileNotFoundError:
            print(f"Erreur : Le fichier est introuvable à l'emplacement : {chemin_image}")
        except Exception as e:
            print(f"Une erreur est survenue : {e}")

# Exemple d'utilisation :
ma_grille = Grille(9)
ma_grille.charger_image()