import random
import copy
import os
from Solver import Solver
from Grille import Grille


class RandomGenerator:

    @staticmethod
    def generate_full_grid(grid):
        """
        Remplit une grille structurelle vide avec des chiffres aléatoires valides.
        """
        return Solver.solve(grid)

    @staticmethod
    def create_puzzle(grid_template, holes_count=20):
        """
        Génère un puzzle à partir d'un modèle fixe.
        """
        puzzle_grid = copy.deepcopy(grid_template)

        if not Solver.solve(puzzle_grid):
            raise Exception("Erreur : Impossible de résoudre cette grille.")

        all_cases = puzzle_grid.get_cases()
        random.shuffle(all_cases)

        count = min(holes_count, len(all_cases))
        for i in range(count):
            all_cases[i].set_value(0)

        return puzzle_grid

    @staticmethod
    def create_random_puzzle_from_folder(folder_path, holes_count=20):
        """
        Choisit UN fichier JSON au hasard dans un dossier, puis génère une solution.
        Ainsi, la FORME du niveau change à chaque fois.
        """
        # 1. Lister tous les fichiers .json dans le dossier
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Le dossier {folder_path} n'existe pas.")

        json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

        if not json_files:
            raise ValueError("Aucun fichier .json trouvé dans le dossier.")

        # 2. Choisir un fichier au hasard
        random_file = random.choice(json_files)
        full_path = os.path.join(folder_path, random_file)

        print(f"Chargement aléatoire de la structure : {random_file}")

        # 3. Charger cette structure
        grid_template = Grille()
        grid_template.load_json(full_path)

        # 4. Générer le puzzle (solution aléatoire + trous)
        return RandomGenerator.create_puzzle(grid_template, holes_count)


# --- Exemple d'utilisation ---
if __name__ == "__main__":
    # Supposons que tu as un dossier "levels" avec grille1.json, grille2.json, etc.
    try:
        # Crée un dossier 'levels' et mets tes json dedans pour tester
        game_grid = RandomGenerator.create_random_puzzle_from_folder("levels", holes_count=10)

        print("\nGrille générée aléatoirement (Structure Chiffres) :")
        print(game_grid)

    except Exception as e:
        print(f"Erreur : {e}")