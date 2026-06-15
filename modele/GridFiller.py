"""Module GridFiller pour le jeu Néonaure.

Étape 1 de la génération aléatoire de niveaux :
remplit une grille N×M de chiffres 1 à 5, en respectant la règle du voisinage
(aucun chiffre identique parmi les 8 voisins).

NB : cette classe ne gère AUCUNE notion de motif. Elle ne remplit que les cases
en respectant la règle 2 du Néonaure (voisinage). Le découpage en motifs est
fait dans une étape suivante (à coder dans MotifGrouper).

Architecture MVC : appartient au Modèle.
"""
import random


DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]


class GridFiller:
    """Remplit une matrice 2D de chiffres 1-5 respectant la règle du voisinage."""

    @staticmethod
    def fill(width=8, height=8, max_value=5):
        """Crée une matrice 2D remplie aléatoirement.

        Args:
            width (int): Largeur de la grille.
            height (int): Hauteur de la grille.
            max_value (int): Valeur maximale (1 à max_value).

        Returns:
            list[list[int]] | None: Matrice 2D des valeurs, ou None si échec.
        """

        matrix = [[0] * width for _ in range(height)]

        if GridFiller._backtrack(matrix, 0, 0, width, height, max_value):
            return matrix
        return None

    @staticmethod
    def _backtrack(matrix, x, y, width, height, max_value):
        """Backtracking : remplit case par case (parcours raster x→, puis y↓).

        Args:
            matrix: la matrice 2D en cours de remplissage.
            x, y: position actuelle.
            width, height: dimensions.
            max_value: valeur max (5 par défaut).

        Returns:
            bool: True si on a réussi à tout remplir.
        """

        if y >= height:
            return True


        next_x = x + 1
        next_y = y
        if next_x >= width:
            next_x = 0
            next_y = y + 1


        values = list(range(1, max_value + 1))
        random.shuffle(values)

        for value in values:
            if GridFiller._is_safe(matrix, x, y, value, width, height):
                matrix[y][x] = value
                if GridFiller._backtrack(
                        matrix, next_x, next_y, width, height, max_value):
                    return True
                matrix[y][x] = 0

        return False

    @staticmethod
    def _is_safe(matrix, x, y, value, width, height):
        """Vérifie qu'aucun voisin (8 directions) n'a déjà cette valeur."""
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if matrix[ny][nx] == value:
                    return False
        return True

    @staticmethod
    def print_matrix(matrix):
        """Affiche joliment la matrice (utile pour débugger)."""
        for row in matrix:
            print(" ".join(str(v) for v in row))


# --- Tests ---
if __name__ == "__main__":
    import time

    print("=== Test 1 : Remplissage 8x8 ===")
    start = time.time()
    m = GridFiller.fill(8, 8)
    elapsed = time.time() - start
    if m:
        GridFiller.print_matrix(m)
        print(f"Rempli en {elapsed:.3f}s")
    else:
        print("Echec")

    print("\n=== Test 2 : Remplissage 6x4 (rectangulaire) ===")
    m = GridFiller.fill(6, 4)
    if m:
        GridFiller.print_matrix(m)

    print("\n=== Test 3 : 20 remplissages 8x8 consecutifs ===")
    total = 0
    fails = 0
    for i in range(20):
        start = time.time()
        m = GridFiller.fill(8, 8)
        elapsed = time.time() - start
        total += elapsed
        if m is None:
            fails += 1
    print(f"20 grilles remplies, total {total:.2f}s "
          f"(moyenne {total/20:.3f}s), echecs : {fails}")

    print("\n=== Test 4 : Verifier qu'aucun chiffre identique ne se touche ===")
    m = GridFiller.fill(8, 8)
    if m:
        ok = True
        for y in range(len(m)):
            for x in range(len(m[0])):
                v = m[y][x]
                for dx, dy in DIRECTIONS:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < len(m[0]) and 0 <= ny < len(m):
                        if m[ny][nx] == v:
                            print(f"BUG : ({x},{y})={v} et "
                                  f"({nx},{ny})={v} se touchent")
                            ok = False
        if ok:
            print("Aucun conflit detecte : OK !")

