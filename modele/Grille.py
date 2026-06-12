"""Module définissant la classe Grille du jeu Néonaure.

Une Grille contient toutes les cases du plateau (valeur 0 si vide)
et la liste des motifs (zones en traits gras). Elle peut être chargée
depuis un fichier JSON et sauvegardée au même format.

Architecture MVC : aucun affichage graphique ici. La méthode __str__
existe uniquement pour le débogage en console.
"""
import json
import os
import sys

try:
    from modele.Case import Case
    from modele.Motif import Motif
except ImportError:
    from Case import Case
    from Motif import Motif


class Grille:
    """Représente une grille complète du Néonaure.

    Attributes:
        width (int): Largeur (nombre de colonnes).
        height (int): Hauteur (nombre de lignes).
        cases (list[Case]): Toutes les cases (vides ou remplies).
        motifs (list[Motif]): Les motifs qui découpent la grille.
    """

    def __init__(self, width=8, height=8):
        """Initialise une grille vide aux dimensions données."""
        self.__width = width
        self.__height = height
        self.__cases = []
        self.__cases_by_pos = {}
        self.__motifs = []
        self.__generate_empty()

    def __generate_empty(self):
        """Crée toutes les cases vides (valeur 0) de la grille."""
        for x in range(self.__width):
            for y in range(self.__height):
                case = Case(x, y, 0)
                self.__cases.append(case)
                self.__cases_by_pos[(x, y)] = case

    # --- Getters ---

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_cases(self):
        return self.__cases

    def get_motifs(self):
        return self.__motifs

    def get_case(self, x, y):
        """Retourne la case en (x, y), ou None. Accès O(1)."""
        return self.__cases_by_pos.get((x, y))

    def get_motif_of(self, x, y):
        """Retourne le motif contenant la case (x, y), ou None."""
        for motif in self.__motifs:
            for case in motif.get_cases():
                if case.get_x() == x and case.get_y() == y:
                    return motif
        return None

    # --- Modifications ---

    def add_motif(self, motif):
        """Ajoute un motif et s'assure que ses cases sont dans la grille."""
        self.__motifs.append(motif)
        for case in motif.get_cases():
            existing = self.get_case(case.get_x(), case.get_y())
            if existing is None:
                self.__cases.append(case)
                self.__cases_by_pos[(case.get_x(), case.get_y())] = case

    def generate_motifs(self, min_size=2, max_size=5, hint_chance=0.25):
        """Génère aléatoirement des motifs couvrant toute la grille."""
        import random
        min_size = max(1, min(min_size, Motif.MAX_SIZE))
        max_size = max(min_size, min(max_size, Motif.MAX_SIZE))

        self.__motifs = []
        for case in self.__cases:
            case.set_value(0)
            case.set_hint(False)

        visited = [[False] * self.__height for _ in range(self.__width)]
        motif_index = 1

        for x in range(self.__width):
            for y in range(self.__height):
                if visited[x][y]:
                    continue

                motif = Motif(f"motif{motif_index}")
                motif_index += 1
                target_size = random.randint(min_size, max_size)

                queue = [(x, y)]
                while queue and motif.get_size() < target_size:
                    idx = random.randint(0, len(queue) - 1)
                    cx, cy = queue.pop(idx)
                    if cx < 0 or cx >= self.__width or cy < 0 or cy >= self.__height:
                        continue
                    if visited[cx][cy]:
                        continue

                    visited[cx][cy] = True
                    case = self.get_case(cx, cy)
                    if case is None:
                        case = Case(cx, cy, 0)
                        self.__cases.append(case)
                        self.__cases_by_pos[(cx, cy)] = case
                    motif.add_case(case)

                    neighbours = [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]
                    random.shuffle(neighbours)
                    for nx, ny in neighbours:
                        if 0 <= nx < self.__width and 0 <= ny < self.__height and not visited[nx][ny]:
                            queue.append((nx, ny))

                size = motif.get_size()
                max_hint = min(size, 5)
                for case in motif.get_cases():
                    if max_hint > 0 and random.random() < hint_chance:
                        val = random.randint(1, max_hint)
                        case.set_value(val)
                        case.set_hint(True)

                self.__motifs.append(motif)

    # --- Persistance JSON ---

    def _get_absolute_path(self, file_path):
        """Sécurise le chemin du fichier au cas où __file__ n'est pas défini."""
        if os.path.isabs(file_path):
            return file_path
        try:
            base = os.path.dirname(os.path.abspath(__file__))
            return os.path.join(base, file_path)
        except NameError:
            return os.path.abspath(file_path)

    def load_json(self, file_path):
        """Charge une grille depuis un fichier JSON.

        Format attendu : {"motif1": [[x,y,v], ...], "motif2": ...}
        """
        file_path = self._get_absolute_path(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.__cases = []
        self.__cases_by_pos = {}
        self.__motifs = []
        max_x, max_y = 0, 0
        for name, cells in data.items():
            motif = Motif(name)
            for cell in cells:
                x, y, value = cell[0], cell[1], cell[2]
                case = Case(x, y, value)
                motif.add_case(case)
                self.__cases.append(case)
                self.__cases_by_pos[(x, y)] = case
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
            self.__motifs.append(motif)
        self.__width = max_x + 1
        self.__height = max_y + 1

    def save_json(self, file_path):
        """Sauvegarde au format JSON des enseignants (compact)."""
        file_path = self._get_absolute_path(file_path)
        data = {}
        for motif in self.__motifs:
            cells = []
            for case in motif.get_cases():
                cells.append([case.get_x(), case.get_y(), case.get_value()])
            data[motif.get_name()] = cells

        # Format compact : chaque motif sur une ligne
        lines = []
        for name, cells in data.items():
            cells_str = ", ".join(f"[{c[0]},{c[1]},{c[2]}]" for c in cells)
            lines.append(f'  "{name}": [{cells_str}]')
        json_content = "{\n" + ",\n".join(lines) + "\n}"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json_content)

    # --- Affichage console (debug) ---

    def __str__(self):
        lines = [
            f"Grille {self.__width} x {self.__height}:",
            f"{len(self.__motifs)} motif(s), {len(self.__cases)} case(s)"
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


# --- Tests ---
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