import random
try:
    from modele.Grille import Grille
    from modele.Case import Case
    from modele.Validator import Validator
except ImportError:
    from Grille import Grille
    from Case import Case
    from Validator import Validator


class Solver:

    @staticmethod
    def solve(grid):
        """
        Résout la grille par backtracking.
        Retourne True si la grille est résolue, False sinon.
        """

        empty_cell = Solver.find_empty_cell(grid)

        if empty_cell is None:
            return True

        x = empty_cell.get_x()
        y = empty_cell.get_y()

        values = list(range(1, 6))  # ← NOUVEAU
        random.shuffle(values)  # ← NOUVEAU
        for value in values:  # ← MODIFIÉ
            is_valid, _ = Validator.check_move(grid, x, y, value)

            if is_valid:

                empty_cell.set_value(value)

                if Solver.solve(grid):
                    return True

                empty_cell.set_value(0)

        return False

    @staticmethod
    def find_empty_cell(grid):
        """
        Retourne la première case vide (valeur 0) trouvée, ou None.
        """
        for case in grid.get_cases():
            if case.get_value() == 0:
                return case
        return None

    @staticmethod
    def get_hint(grid):
        """
        Donne un indice : résout la grille, retourne (x, y, value) pour
        la première case vide, puis restaure la grille. Retourne None si
        aucune solution n'existe.
        """
        original_values = {}
        for case in grid.get_cases():
            original_values[(case.get_x(), case.get_y())] = case.get_value()

        if Solver.solve(grid):
            for (x, y), orig_val in original_values.items():
                if orig_val == 0:
                    case = grid.get_case(x, y)
                    hint_value = case.get_value()
                    for (rx, ry), rv in original_values.items():
                        grid.get_case(rx, ry).set_value(rv)
                    return x, y, hint_value

        for (x, y), v in original_values.items():
            grid.get_case(x, y).set_value(v)
        return None


"""
if __name__ == "__main__":

    from Motif import Motif

    if __name__ == "__main__":
        print("--- Test du Solver ---")


        g = Grille(2, 2)

        m = Motif("M1")
        m.add_case(g.get_case(0, 0))
        m.add_case(g.get_case(1, 0))
        m.add_case(g.get_case(0, 1))
        m.add_case(g.get_case(1, 1))
        g.add_motif(m)

        print("Avant résolution :")
        print(g)

        if Solver.solve(g):
            print("\nGrille résolue :")
            print(g)
        else:
            print("\nImpossible de résoudre.")
 """
if __name__ == "__main__":
    g = Grille()
    g.load_json("grille1.json")

    print("Avant résolution :")
    print(g)
    if Solver.solve(g):
        print("\nGrille résolue :")
        print(g)
    else:
        print("\nImpossible de résoudre.")