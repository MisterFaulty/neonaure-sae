"""Module définissant la classe Grille du jeu Néonaure.

Une Grille contient toutes les cases du plateau (valeur 0 si vide)
et la liste des motifs (zones en traits gras). Elle peut être chargée
depuis un fichier JSON et sauvegardée au même format.

Architecture MVC : aucun affichage graphique ici. La méthode __str__
existe uniquement pour le débogage en console.
"""
import json
from Case import Case
from Motif import Motif

class Grille:
    def __init__(self,width = 8, height = 8 ):
        self.__height = height
        self.__width = width
        self.__cases = []
        self.__motifs = []
        self.__generate_empty()


    def __generate_empty(self):

        for x in range(self.__width):
            for y in range(self.__height):
                self.__cases.append(Case(x,y,0))

#   --- Getters ---
    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_cases(self):
        return self.__cases

    def get_motifs(self):
        return self.__motifs

    def get_case(self,x,y):
        for case in self.__cases:
            if case.get_x() == x and case.get_y() == y:
                return case
        return None

    def get_motif_of(self,x,y):
        for motif in self.__motifs:
            for case in self.__cases:
                if case.get_x() == x and case.get_y() == y:
                    return motif
        return None


    def add_motif(self,motif):
        self.__motifs.append(motif)

    def load_json(self,file_path):
        with open(file_path,"r" , encoding='utf-8') as f:
            data = json.load(f)

        self.__cases = []
        self.__motifs = []
        max_x,max_y = 0,0
        for name,cells in data.items():
            motif = Motif(name)
            for cell in cells:
                x,y,value = cell[0],cell[1],cell[2]
                case = Case(x,y,value)
                motif.add_case(case)
                self.__cases.append(case)
                if x >max_x:
                    max_x = x
                if y >max_y:
                    max_y = y
            self.__motifs.append(motif)
        self.__width = max_x+1
        self.__height = max_y+1




    def save_json(self,file_path):
        data = {}
        for motif in self.__motifs:
            cells = []
            for cases in motif.get_case():
                cells.append([cases.get_x(),cases.get_y(),cases.get_value()])
            data[motif.get_name()] = cells
        with open(file_path,"w" , encoding='utf-8') as f:
            json.dump(data, f, indent=2)


    def __str__(self):
        lines = [
            f"Grille {self.__width} x {self.__height}:",
            f"{len(self.__motifs)} motif(s),{len(self.__cases)} case(s)"
        ]
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                case = self.get_case(x, y)
                if case is None:
                    row.append(".")
                else:
                    v = case.get_value()
                    row.append(str(v) if v != 0 else "·")
            lines.append(" ".join(row))
        return "\n".join(lines)



if __name__ == "__main__":
    print("=== Test 1 : Grille vide 8x8 ===")
    g = Grille()
    print(f"Dimensions : {g.get_width()} x {g.get_height()}")
    print(f"Nombre de cases : {len(g.get_cases())}")

    print("\n=== Test 2 : Chargement de grille1.json ===")
    g2 = Grille()
    g2.load_json("grille1.json")
    print(g2)

    print("\n=== Test 3 : Case (1,1) ===")
    c = g2.get_case(1, 1)
    print(f"Case trouvée : {c}")

    print("\n=== Test 4 : Motif contenant (1,1) ===")
    m = g2.get_motif_of(1, 1)
    print(f"Motif : {m.get_name() if m else None}")

    print("\n=== Test 5 : Sauvegarde ===")
    g2.save_json("grille_save.json")
    print("Fichier sauvegardé.")

    print("\n=== Test 6 : Grille rectangulaire 6x4 ===")
    g3 = Grille(6, 4)
    print(f"Dimensions : {g3.get_width()} x {g3.get_height()}")
    print(f"Nombre de cases : {len(g3.get_cases())}")





