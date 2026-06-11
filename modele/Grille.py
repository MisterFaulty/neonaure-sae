"""Module définissant la classe Grille du jeu Néonaure.

Une Grille contient toutes les cases du plateau (valeur 0 si vide)
et la liste des motifs (zones en traits gras). Elle peut être chargée
depuis un fichier JSON et sauvegardée au même format.

Architecture MVC : aucun affichage graphique ici. La méthode __str__
existe uniquement pour le débogage en console.
"""
import json
import os
import random
import sys

# Ajouter le dossier contenant ce fichier au sys.path pour permettre les imports directs de Case et Motif
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from Case import Case
from Motif import Motif


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
        for case in self.__cases:
            if case.get_x() == x and case.get_y() == y:
                return case
        return None

    def _get_motif_cases(self, motif):
        """Retourne la liste des cases d'un motif en gérant get_case() et get_cases()."""
        return motif.get_cases() if hasattr(motif, 'get_cases') else motif.get_case()

    def get_motif_of(self, x, y):
        """Retourne le motif contenant la case (x, y), ou None."""
        for motif in self.__motifs:
            for case in self._get_motif_cases(motif):
                if case.get_x() == x and case.get_y() == y:
                    return motif
        return None

    def add_motif(self, motif):
        self.__motifs.append(motif)
        # S'assurer que les cases du motif existent dans la grille
        for case in self._get_motif_cases(motif):
            existing = self.get_case(case.get_x(), case.get_y())
            if existing is None:
                self.__cases.append(case)

    # ------------------------------------------------------------------
    #  Création de motifs à partir de données [[x, y, value], ...]
    # ------------------------------------------------------------------
    def create_motif(self, name, cells_data):
        """Crée un motif à partir d'une liste de [x, y, value] et l'ajoute.

        Les valeurs doivent être comprises entre 0 et 5.
        Le nombre de cases ne peut pas dépasser Motif.MAX_SIZE (5).

        Args:
            name:       nom du motif (ex. "motif1")
            cells_data: liste de listes [x, y, value]

        Returns:
            Motif: le motif créé

        Raises:
            ValueError: si une valeur est > 5 ou si le motif
                        dépasse Motif.MAX_SIZE cases
        """
        motif = Motif(name)
        for cell in cells_data:
            x, y, value = cell[0], cell[1], cell[2]
            case = self.get_case(x, y)
            if case is not None:
                case.set_value(value)  # Lève ValueError si value > 5
            else:
                case = Case(x, y, value)  # Lève ValueError si value > 5
                self.__cases.append(case)
            motif.add_case(case)  # Lève ValueError si > MAX_SIZE
        self.__motifs.append(motif)
        return motif

    # ------------------------------------------------------------------
    #  Génération automatique de motifs couvrant toute la grille
    # ------------------------------------------------------------------
    def generate_motifs(self, min_size=2, max_size=5, hint_chance=0.25):
        """Génère automatiquement des motifs qui couvrent toute la grille.

        Chaque case appartient à exactement un motif. Les motifs ont une
        taille aléatoire entre min_size et max_size (borné par
        Motif.MAX_SIZE). Certaines cases reçoivent une valeur (indice)
        comprise entre 1 et la taille du motif, selon hint_chance.

        Args:
            min_size:    taille minimale d'un motif (défaut 2, max 5)
            max_size:    taille maximale d'un motif (défaut 5, max 5)
            hint_chance: probabilité qu'une case reçoive un indice (défaut 0.25)
        """
        # Bornes de sécurité
        min_size = max(1, min(min_size, Motif.MAX_SIZE))
        max_size = max(min_size, min(max_size, Motif.MAX_SIZE))

        self.__motifs = []
        # Réinitialiser toutes les cases à 0
        for case in self.__cases:
            case.set_value(0)

        # Grille de visite pour savoir quelles cases sont déjà assignées
        visited = [[False] * self.__height for _ in range(self.__width)]
        motif_index = 1

        for x in range(self.__width):
            for y in range(self.__height):
                if visited[x][y]:
                    continue

                # Débuter un nouveau motif depuis (x, y)
                motif = Motif(f"motif{motif_index}")
                motif_index += 1
                target_size = random.randint(min_size, max_size)

                # Croissance en flood-fill aléatoire
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
                    if case is None:
                        case = Case(cx, cy, 0)
                        self.__cases.append(case)
                    motif.add_case(case)

                    # Voisins orthogonaux mélangés
                    neighbours = [(cx + 1, cy), (cx - 1, cy),
                                  (cx, cy + 1), (cx, cy - 1)]
                    random.shuffle(neighbours)
                    for nx, ny in neighbours:
                        if 0 <= nx < self.__width and 0 <= ny < self.__height:
                            if not visited[nx][ny]:
                                queue.append((nx, ny))

                # Assigner des indices (valeurs 1..taille_du_motif)
                # Un indice doit être <= taille du motif et <= 5 (max Case)
                size = motif.get_size()
                max_hint = min(size, 5)
                for case in self._get_motif_cases(motif):
                    if max_hint > 0 and random.random() < hint_chance:
                        case.set_value(random.randint(1, max_hint))

                self.__motifs.append(motif)

    # ------------------------------------------------------------------
    #  Création de motifs à partir d'un dictionnaire (format JSON)
    # ------------------------------------------------------------------
    def create_motifs_from_dict(self, data):
        """Crée plusieurs motifs à partir d'un dictionnaire {nom: [[x,y,v], ...]}.

        Réinitialise la grille (cases et motifs) puis crée les motifs
        depuis le dictionnaire. Les valeurs doivent être entre 0 et 5,
        et chaque motif ne doit pas dépasser Motif.MAX_SIZE cases.

        Args:
            data: dict tel que {"motif1": [[0,0,0],[1,0,3], ...], ...}

        Raises:
            ValueError: si une valeur est > 5 ou si un motif
                        dépasse Motif.MAX_SIZE cases
        """
        self.__cases = []
        self.__motifs = []
        max_x, max_y = 0, 0
        for name, cells_data in data.items():
            motif = Motif(name)
            for cell in cells_data:
                x, y, value = cell[0], cell[1], cell[2]
                case = Case(x, y, value)  # ValueError si value > 5
                motif.add_case(case)       # ValueError si > MAX_SIZE
                self.__cases.append(case)
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
            self.__motifs.append(motif)
        self.__width = max_x + 1
        self.__height = max_y + 1

    # ------------------------------------------------------------------
    #  Chargement / Sauvegarde JSON
    # ------------------------------------------------------------------
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
        """Charge une grille depuis un fichier JSON.

        Le format attendu est : {"motif1": [[x,y,v], ...], "motif2": ...}
        Les valeurs doivent être entre 0 et 5.
        Chaque motif ne doit pas dépasser Motif.MAX_SIZE cases.
        """
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
                case = Case(x, y, value)  # ValueError si value > 5
                motif.add_case(case)       # ValueError si > MAX_SIZE
                self.__cases.append(case)
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
            self.__motifs.append(motif)
        self.__width = max_x + 1
        self.__height = max_y + 1

    def save_json(self, file_path):
        """Sauvegarde la grille au format JSON compatible avec load_json."""
        file_path = self._get_absolute_path(file_path)
        data = {}
        for motif in self.__motifs:
            cells = []
            for case in self._get_motif_cases(motif):
                cells.append([case.get_x(), case.get_y(), case.get_value()])
            data[motif.get_name()] = cells

        # Custom JSON formatting to keep the coordinate lists compact on one line
        lines = []
        for name, cells in data.items():
            cells_str = ", ".join(f"[{c[0]},{c[1]},{c[2]}]" for c in cells)
            lines.append(f'  "{name}": [{cells_str}]')
        
        json_content = "{\n" + ",\n".join(lines) + "\n}"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json_content)

    # ------------------------------------------------------------------
    #  Export en dictionnaire (utile pour manipulation avant sauvegarde)
    # ------------------------------------------------------------------
    def to_dict(self):
        """Retourne la grille sous forme de dictionnaire {nom: [[x,y,v], ...]}."""
        data = {}
        for motif in self.__motifs:
            cells = []
            for case in self._get_motif_cases(motif):
                cells.append([case.get_x(), case.get_y(), case.get_value()])
            data[motif.get_name()] = cells
        return data

    # ------------------------------------------------------------------
    #  Affichage console (débogage)
    # ------------------------------------------------------------------
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
    print("=== Test 1 : Génération aléatoire d'une grille 8x8 ===")
    g = Grille(8, 8)
    g.generate_motifs(min_size=2, max_size=5, hint_chance=0.25)
    print(f"Dimensions : {g.get_width()} x {g.get_height()}")
    print(f"Nombre de cases : {len(g.get_cases())}")
    g.save_json("grille_manuelle.json")
    print("→ Sauvegardé une grille aléatoire dans grille_manuelle.json\n")

    print("\n=== Test 2 : Chargement de la grille générée ===")
    g2 = Grille()
    g2.load_json("grille_manuelle.json")
    print(g2)

    print("\n=== Test 3 : Case (1,1) ===")
    c = g2.get_case(1, 1)
    print(f"Case trouvée : {c}")

    print("\n=== Test 4 : Motif contenant (1,1) ===")
    m = g2.get_motif_of(1, 1)
    print(f"Motif : {m.get_name() if m else None}")

    print("\n=== Test 5 : Sauvegarde de vérification ===")
    g2.save_json("grille_save.json")
    print("Fichier grille_save.json sauvegardé.")

    print("\n=== Test 6 : Grille rectangulaire 6x4 ===")
    g3 = Grille(6, 4)
    print(f"Dimensions : {g3.get_width()} x {g3.get_height()}")




