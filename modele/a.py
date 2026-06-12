import json
import os
import random
<<<<<<< Updated upstream
try:
    from modele.Case import Case
    from modele.Motif import Motif
except ImportError:
    from Case import Case
    from Motif import Motif
=======
from Case import Case
from Motif import Motif
>>>>>>> Stashed changes

class Grille:
    def __init__(self, width=8, height=8):
        self.__height = height
        self.__width = width
        self.__cases = []
        self.__motifs = []
        self.__generate_empty()

    def __generate_empty(self):
        for x in range(self.__width):
            for y in range(self.__height):
                self.__cases.append(Case(x, y, 0))

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_cases(self):
        return self.__cases

    def get_motifs(self):
        return self.__motifs

    def get_case(self, x, y):
        for case in self.__cases:
            if case.get_x() == x and case.get_y() == y:
                return case
        return None

    def get_motif_of(self, x, y):
        for motif in self.__motifs:
            if motif.contains(x, y):
                return motif
        return None

    def add_motif(self, motif):
        self.__motifs.append(motif)
        for case in motif.get_cases():  # CORRECTION: get_cases() au pluriel
            existing = self.get_case(case.get_x(), case.get_y())
            if existing is None:
                self.__cases.append(case)

    def create_motif(self, name, cells_data):
        motif = Motif(name)
        for cell in cells_data:
            x, y, value = cell[0], cell[1], cell[2]
            case = self.get_case(x, y)
            if case is not None:
                case.set_value(value)
            else:
                case = Case(x, y, value)
                self.__cases.append(case)
            motif.add_case(case)
        self.__motifs.append(motif)
        return motif

    def generate_motifs(self, min_size=2, max_size=5, hint_chance=0.25):
        min_size = max(1, min(min_size, Motif.MAX_SIZE))
        max_size = max(min_size, min(max_size, Motif.MAX_SIZE))

        self.__motifs = []
        for case in self.__cases:
            case.set_value(0)

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
                    if cx < 0 or cx >= self.__width:
                        continue
                    if cy < 0 or cy >= self.__height:
                        continue
                    if visited[cx][cy]:
                        continue

                    visited[cx][cy] = True
                    case = self.get_case(cx, cy)
                    motif.add_case(case)

                    neighbours = [(cx + 1, cy), (cx - 1, cy),
                                  (cx, cy + 1), (cx, cy - 1)]
                    random.shuffle(neighbours)
                    for nx, ny in neighbours:
                        if 0 <= nx < self.__width and 0 <= ny < self.__height:
                            if not visited[nx][ny]:
                                queue.append((nx, ny))

                size = motif.get_size()
                max_hint = min(size, 5)
                for case in motif.get_cases():  # CORRECTION: get_cases() au pluriel
                    if max_hint > 0 and random.random() < hint_chance:
                        case.set_value(random.randint(1, max_hint))

                self.__motifs.append(motif)

    def create_motifs_from_dict(self, data):
        self.__cases = []
        self.__motifs = []
        max_x, max_y = 0, 0
        for name, cells_data in data.items():
            motif = Motif(name)
            for cell in cells_data:
                x, y, value = cell[0], cell[1], cell[2]
                case = Case(x, y, value)
                motif.add_case(case)
                self.__cases.append(case)
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
            self.__motifs.append(motif)
        self.__width = max_x + 1
        self.__height = max_y + 1

    def _get_absolute_path(self, file_path):
        """Sécurise le chemin du fichier au cas où __file__ n'est pas défini."""
        if os.path.isabs(file_path):
            return file_path
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            return os.path.join(base_dir, file_path)
        except NameError:
            return os.path.abspath(file_path)

    def load_json(self, file_path):
        file_path = self._get_absolute_path(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.__cases = []
        self.__motifs = []
        max_x, max_y = 0, 0
        for name, cells in data.items():
            motif = Motif(name)
            for cell in cells:
                x, y, value = cell[0], cell[1], cell[2]
                case = Case(x, y, value)
                motif.add_case(case)
                self.__cases.append(case)
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
            self.__motifs.append(motif)
        self.__width = max_x + 1
        self.__height = max_y + 1

    def save_json(self, file_path):
        file_path = self._get_absolute_path(file_path)
        data = {}
        for motif in self.__motifs:
            cells = []
            for case in motif.get_cases():  # CORRECTION: get_cases() au pluriel
                cells.append([case.get_x(), case.get_y(), case.get_value()])
            data[motif.get_name()] = cells
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def to_dict(self):
        data = {}
        for motif in self.__motifs:
            cells = []
            for case in motif.get_cases():  # CORRECTION: get_cases() au pluriel
                cells.append([case.get_x(), case.get_y(), case.get_value()])
            data[motif.get_name()] = cells
        return data

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


if __name__ == "__main__":
    random.seed(42)

    print("=== Test 1 : Création manuelle de plusieurs motifs ===")
    g1 = Grille(8, 8)
    g1.create_motif("motif1", [[0, 0, 0], [1, 0, 0], [0, 1, 0],
                               [1, 1, 3], [2, 1, 0]])
    g1.create_motif("motif2", [[2, 0, 5], [3, 0, 0], [4, 0, 0],
                               [4, 1, 0], [5, 0, 0]])
    g1.create_motif("motif3", [[6, 0, 0], [5, 1, 0], [6, 1, 4],
                               [6, 2, 0], [7, 0, 0]])
    g1.create_motif("motif4", [[0, 2, 5], [1, 2, 0], [0, 3, 0],
                               [1, 3, 0], [0, 4, 0]])
    g1.create_motif("motif5", [[2, 2, 0], [2, 3, 0], [3, 1, 0],
                               [3, 2, 0], [4, 2, 0]])
    g1.create_motif("motif6", [[5, 2, 0], [4, 3, 0], [5, 3, 5],
                               [4, 4, 0], [5, 4, 0]])
    g1.create_motif("motif7", [[7, 3, 0], [6, 4, 0], [7, 4, 2],
                               [7, 5, 0], [7, 6, 0]])
    g1.create_motif("motif8", [[0, 5, 0], [0, 6, 0], [1, 5, 3],
                               [1, 4, 0], [2, 4, 0]])
    g1.create_motif("motif9", [[2, 5, 0], [3, 5, 0], [4, 5, 0],
                               [3, 4, 0], [3, 3, 0]])
    g1.create_motif("motif10", [[0, 7, 3], [1, 6, 0], [1, 7, 0],
                                [2, 6, 5], [2, 7, 0]])
    g1.create_motif("motif11", [[7, 1, 0], [7, 2, 0]])
    g1.create_motif("motif12", [[3, 6, 0], [4, 6, 0], [3, 7, 0],
                                [4, 7, 0], [5, 7, 2]])
    g1.create_motif("motif13", [[5, 6, 0], [6, 5, 0], [6, 6, 0],
                                [6, 7, 0], [7, 7, 0]])
    g1.create_motif("motif14", [[6, 3, 0]])
    g1.create_motif("motif15", [[5, 5, 0]])
    print(g1)
    g1.save_json("grille_manuelle.json")
    print("→ Sauvegardé dans grille_manuelle.json\n")

    print("=== Test 2 : Création depuis un dictionnaire ===")
    data = {
        "zone_A": [[0, 0, 2], [1, 0, 0], [0, 1, 0]],
        "zone_B": [[2, 0, 0], [3, 0, 5], [2, 1, 0], [3, 1, 0]],
        "zone_C": [[0, 2, 0], [1, 2, 3], [0, 3, 0], [1, 3, 0]],
        "zone_D": [[2, 2, 0], [3, 2, 0], [2, 3, 4], [3, 3, 0]],
    }
    g2 = Grille(4, 4)
    g2.create_motifs_from_dict(data)
    print(g2)
    g2.save_json("grille_dict.json")
    print("→ Sauvegardé dans grille_dict.json\n")

    print("=== Test 3 : Génération automatique de motifs (8x8) ===")
    g3 = Grille(8, 8)
    g3.generate_motifs(min_size=2, max_size=5, hint_chance=0.25)
    print(g3)
    print(f"Nombre de motifs générés : {len(g3.get_motifs())}")
    for m in g3.get_motifs():
        print(f"  {m.get_name()} : {m.get_size()} cases")
    g3.save_json("grille_auto.json")
    print("→ Sauvegardé dans grille_auto.json\n")

    print("=== Test 4 : Round-trip save → load ===")
    g4 = Grille()
    g4.load_json("grille_manuelle.json")
    print(g4)
    g4.save_json("grille_reloaded.json")
    print("→ Re-sauvegardé dans grille_reloaded.json\n")

    print("=== Test 5 : Export to_dict() ===")
    d = g2.to_dict()
    print(json.dumps(d, indent=2))