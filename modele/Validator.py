"""
Module Validator for the Neonaure game.

Uses static methods as no instance state is required.
"""

class Validator:

    @staticmethod
    def check_move(grid, x, y, value):
        """
        Checks if placing 'value' at (x, y) is a valid move.
        Returns a tuple (bool, str_message).
        """

        # 0. Basic Value check
        if not (1 <= value <= 5):
            return False, "Value must be between 1 and 5."

        # 1. Check Motif Rules (Uniqueness and Size)
        motif = grid.get_motif_of(x, y)
        if motif is None:
            return False, "Cell does not belong to any motif."

        motif_cells = motif.get_cases()
        motif_size = len(motif_cells)

        # Rule: If motif size is 3, allowed values are 1, 2, 3.
        if value > motif_size:
            return False, f"Motif size is {motif_size}, max value allowed is {motif_size}."

        # Rule: Unique value inside the motif
        for cell in motif_cells:
            if cell.get_x() == x and cell.get_y() == y:
                continue

            if cell.get_value() == value:
                return False, f"Value {value} is already present in this motif."

        # 2. Check Neighbor Rule (No-Touch / King's Move)
        is_valid, message = Validator._check_neighbors(grid, x, y, value)
        if not is_valid:
            return False, message

        return True, "Move valid."

    @staticmethod
    def _check_neighbors(grid, x, y, value):
        """Private static method to check the 8 surrounding cells."""
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                neighbor = grid.get_case(x + dx, y + dy)

                if neighbor is not None and neighbor.get_value() == value:
                    return False, f"Value {value} touches an identical neighbor."

        return True, ""

    @staticmethod
    def check_grid_complete(grid):
        """Checks if the whole grid is correctly filled (Win condition)."""
        for cell in grid.get_cases():
            if cell.get_value() == 0:
                return False, "Grid is incomplete."

            is_valid, msg = Validator.check_move(grid, cell.get_x(), cell.get_y(), cell.get_value())
            if not is_valid:
                return False, f"Conflict at ({cell.get_x()},{cell.get_y()}): {msg}"

        return True, "Grid is perfect!"


if __name__ == "__main__":
    from Grille import Grille
    from Case import Case
    from Motif import Motif

    print("--- Running Validator Tests ---")

    g = Grille(2, 2)

    motif_a = Motif("Row 0")
    motif_a.add_case(Case(0, 0, 0))
    motif_a.add_case(Case(1, 0, 0))
    motif_a.add_case(Case(2, 0, 0))

    motif_b = Motif("Row 1")
    motif_b.add_case(Case(0, 1, 0))
    motif_b.add_case(Case(1, 1, 0))
    motif_b.add_case(Case(2, 1, 0))

    g.add_motif(motif_a)
    g.add_motif(motif_b)

    # No need for val = Validator(), call directly on class
    is_valid, message = Validator.check_move(g, 0, 0, 1)
    print(f"Test 1 (Place 1 at 0,0): {is_valid} - {message}")

    if is_valid:
        g.get_case(0, 0).set_value(1)

    is_valid, message = Validator.check_move(g, 1, 0, 1)
    print(f"Test 2 (Place 1 at 1,0 - same motif): {is_valid} - {message}")

    is_valid, message = Validator.check_move(g, 2, 0, 4)
    print(f"Test 3 (Place 4 at 2,0 - too large): {is_valid} - {message}")

    is_valid, message = Validator.check_move(g, 1, 1, 1)
    print(f"Test 4 (Place 1 at 1,1 - neighbor): {is_valid} - {message}")