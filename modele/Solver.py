import random
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

        motif = grid.get_motif_of(x, y)
        motif_size = motif.get_size() if motif else 5

        values = list(range(1, motif_size + 1))
        random.shuffle(values)
        for value in values:
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
        Trouve la case vide qui a le moins de valeurs possibles (MRV heuristic).
        """
        best_case = None
        min_options = 999
        
        for case in grid.get_cases():
            if case.get_value() == 0:
                x = case.get_x()
                y = case.get_y()
                motif = grid.get_motif_of(x, y)
                motif_size = motif.get_size() if motif else 5
                
                valid_count = 0
                for value in range(1, motif_size + 1):
                    is_valid, _ = Validator.check_move(grid, x, y, value)
                    if is_valid:
                        valid_count += 1
                
                if valid_count < min_options:
                    min_options = valid_count
                    best_case = case
                    if min_options == 0:
                        return case
        return best_case

    @staticmethod
    def get_hint(grid):
        """
        Trouve une case vide dans la grille et retourne un indice sous la forme (x, y, value).
        Retourne None si la grille est déjà résolue ou insoluble.
        """
        import copy
        # On copie la grille pour ne pas modifier l'originale lors de la résolution
        grid_copy = copy.deepcopy(grid)

        # On tente de résoudre la copie de la grille
        if not Solver.solve(grid_copy):
            return None

        # On cherche toutes les cases vides dans la grille originale
        empty_cases = [c for c in grid.get_cases() if c.get_value() == 0]
        if not empty_cases:
            return None

        # On en choisit une au hasard
        target_case = random.choice(empty_cases)
        x = target_case.get_x()
        y = target_case.get_y()

        # On récupère la valeur résolue correspondante
        solved_case = grid_copy.get_case(x, y)
        if solved_case:
            return x, y, solved_case.get_value()

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