"""Creation de la classe Grille du jeu Neonaure."""
import json
from modele.Case import Case
from modele.Motif import Motif


class Grille:
    def __init__(self, taille=9):
        self.taille = taille
        self.__cases = []
        self.__motifs = []
        self.__generer_grille_vide()

    def __generer_grille_vide(self):
        for x in range(self.taille):
            for y in range(self.taille):
                self.__cases.append(Case(x, y, 0))

    

    def get_case(self, x, y):
        for case in self.__cases:
            if case.get_x() == x and case.get_y() == y:
                return case
        return None

    def get_cases(self):
        return self.__cases

    def get_motifs(self):
        return self.__motifs

    

    def ajouter_motif(self, motif):
        self.__motifs.append(motif)

    def exporter_json(self, nom_fichier="grille_sudoku.json"):
        donnees = {"cases": [], "motifs": []}

        for case in self.__cases:
            donnees["cases"].append([case.get_x(), case.get_y(), case.get_value()])

        for motif in self.__motifs:
            motif_data = {
                "nom": motif.get_name(),
                "cases": [[c.get_x(), c.get_y()] for c in motif.get_case()]
            }
            donnees["motifs"].append(motif_data)

        with open(nom_fichier, 'w', encoding='utf-8') as f:
            json.dump(donnees, f, indent=4)
        print(f"Grille exportée dans : {nom_fichier}")

    def charger_json(self, nom_fichier="grille_sudoku.json"):
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            donnees = json.load(f)

        for case_data in donnees["cases"]:
            x, y, valeur = case_data
            case = self.get_case(x, y)
            if case is not None:
                case.set_value(valeur)

        self.__motifs = []
        for motif_data in donnees["motifs"]:
            motif = Motif(motif_data["nom"])
            for coord in motif_data["cases"]:
                x, y = coord
                case = self.get_case(x, y)
                if case is not None:
                    motif.add_case(case)
            self.__motifs.append(motif)
        print(f"Grille chargée depuis : {nom_fichier}")

    

    def __str__(self):
        lignes = []
        for x in range(self.taille):
            ligne = ""
            for y in range(self.taille):
                case = self.get_case(x, y)
                val = case.get_value() if case.get_value() != 0 else "."
                ligne += f"{val} "
            lignes.append(ligne)
        return "\n".join(lignes)


# --- Test ---
if __name__ == "__main__":
    g = Grille(9)
    print(g)
    print(f"\nNombre de cases : {len(g.get_cases())}")

    m1 = Motif("motif1")
    m1.add_case(g.get_case(0, 0))
    m1.add_case(g.get_case(0, 1))
    m1.add_case(g.get_case(1, 0))
    g.ajouter_motif(m1)

    g.exporter_json()
    g.charger_json()
    print(f"Motifs chargés : {len(g.get_motifs())}")
