"""Module LevelGenerator pour le jeu Néonaure.

Charge les niveaux pré-faits depuis le dossier ressources/.
Chaque niveau est un fichier JSON au format des grilles fournies par les
enseignants.

Architecture MVC : fait partie du Modèle. Aucune dépendance à la Vue ou
au Contrôleur.
"""
import os
<<<<<<< Updated upstream
try:
    from modele.Grille import Grille
except ImportError:
    from Grille import Grille
=======
from Grille import Grille
>>>>>>> Stashed changes


class LevelGenerator:
    """Gère les niveaux pré-faits du mode Campagne."""

    LEVELS_COUNT = 5

    DIFFICULTY = {
        1: "easy",
        2: "easy",
        3: "medium",
        4: "medium",
        5: "hard",
    }

    @staticmethod
    def _get_ressources_dir():
        """Retourne le chemin du dossier ressources/ a la racine du projet."""
        base = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(base)
        return os.path.join(project_root, "ressources")

    @staticmethod
    def get_levels_count():
        """Retourne le nombre total de niveaux disponibles."""
        return LevelGenerator.LEVELS_COUNT

    @staticmethod
    def get_difficulty(level_number):
        """Retourne la difficulte d'un niveau ('easy', 'medium', 'hard')."""
        if level_number not in LevelGenerator.DIFFICULTY:
            raise ValueError(
                f"Niveau invalide : {level_number}. "
                f"Doit etre entre 1 et {LevelGenerator.LEVELS_COUNT}."
            )
        return LevelGenerator.DIFFICULTY[level_number]

    @staticmethod
    def get_level(level_number):
        """Charge le niveau N et retourne une Grille prete a jouer.

        Args:
            level_number (int): Numero du niveau (1 a LEVELS_COUNT).

        Returns:
            Grille: La grille du niveau.

        Raises:
            ValueError: Si le numero est invalide.
            FileNotFoundError: Si le fichier n'existe pas.
        """
        if not (1 <= level_number <= LevelGenerator.LEVELS_COUNT):
            raise ValueError(
                f"Niveau invalide : {level_number}. "
                f"Doit etre entre 1 et {LevelGenerator.LEVELS_COUNT}."
            )

        ressources_dir = LevelGenerator._get_ressources_dir()
        file_path = os.path.join(ressources_dir, f"level_{level_number}.json")

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Fichier de niveau introuvable : {file_path}"
            )

        grid = Grille()
        grid.load_json(file_path)
        return grid

    @staticmethod
    def get_all_levels_info():
        """Retourne la liste des infos pour tous les niveaux."""
        infos = []
        ressources_dir = LevelGenerator._get_ressources_dir()
        for n in range(1, LevelGenerator.LEVELS_COUNT + 1):
            file_path = os.path.join(ressources_dir, f"level_{n}.json")
            infos.append({
                "numero": n,
                "difficulty": LevelGenerator.DIFFICULTY[n],
                "available": os.path.exists(file_path),
            })
        return infos


# --- Tests ---
if __name__ == "__main__":
    print("=== Test 1 : Liste de tous les niveaux ===")
    for info in LevelGenerator.get_all_levels_info():
        marker = "OK" if info["available"] else "MANQUANT"
        print(f"  [{marker}] Niveau {info['numero']} ({info['difficulty']})")

    print(f"\nTotal : {LevelGenerator.get_levels_count()} niveaux")

    print("\n=== Test 2 : Chargement du niveau 1 ===")
    try:
        g1 = LevelGenerator.get_level(1)
        print(f"Difficulte : {LevelGenerator.get_difficulty(1)}")
        print(g1)
    except Exception as e:
        print(f"Erreur : {e}")

    print("\n=== Test 3 : Chargement du niveau 5 ===")
    try:
        g5 = LevelGenerator.get_level(5)
        print(f"Difficulte : {LevelGenerator.get_difficulty(5)}")
        print(g5)
    except Exception as e:
        print(f"Erreur : {e}")

    print("\n=== Test 4 : Numero de niveau invalide ===")
    try:
        LevelGenerator.get_level(99)
    except ValueError as e:
        print(f"Erreur correctement levee : {e}")