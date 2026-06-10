"""Creation de  la classe motif du jeu neonaure

    Un Motif est un ensemble de cases (entre 1 et 5) qui doit, dans une
    grille résolue, contenir tous les chiffres de 1 à N (N = taille du motif).
    Les frontières d'un motif sont représentées par des traits gras sur la grille.

"""
from Case import  Case




class Motif:
    MAX_SIZE = 5

    """Représente un motif (zone en traits gras) de la grille Néonaure.

    Attributes:
        name (str): Identifiant du motif (ex: "motif1").
        cases (list[Case]): Liste des cases appartenant au motif.
    """

    def __init__(self,name):

        """Initialise un motif vide avec son nom.
            Args:
                name (str): Identifiant du motif (ex: "motif1").
        """


        self.__name = name
        self.__case = []

#   --- Getters ---


    def get_name(self):
        """Retourne le nom du motif."""
        return self.__name

    def get_case(self):
        """Retourne la liste des cases du motif."""
        return self.__case

    def get_size(self):
        """Retourne le nombre de cases du motif."""
        return len(self.__case)


#   --- Methodes ---

    def add_case(self,case):
        """Ajoute une case au motif.
        Args:
            case (Case): La case à ajouter.
        Raises:
            ValueError: Si le motif a déjà atteint sa taille maximale (5).
        """

        if self.get_size() >= Motif.MAX_SIZE:
            raise ValueError(f"A motif cannot exceed {Motif.MAX_SIZE} cases")
        self.__case.append(case)

    def contains_value(self,value):
        """Vérifie si une valeur est déjà présente dans le motif.

        Args:
            value (int): La valeur à chercher.

        Returns:
            bool: True si au moins une case du motif contient cette valeur.
        """

        for case in self.__case:
            if case.get_value() == value:
                return True
        return False
#   --- Representation ---

    def __str__(self):
        """Retourne une représentation lisible du motif."""
        cases_str = ",".join(str(c) for c in self.__case)
        return f"Motif:({self.__name} , {self.get_size()} , cases) : [{cases_str}]"


#T  --- Test ---

if __name__ == "__main__":
    m1 = Motif("motif1")
    m1.add_case(Case(0,0,1))
    m1.add_case(Case(1,0,2))
    m1.add_case(Case(1,1,4))
    m1.add_case(Case(0,1,3))
    print(m1)


    print("La taille de la motif est :", m1.get_size())
    print("Le motif contient-il un 4 ?", m1.contains_value(4))
    print("Le motif contient-il un 5 ?", m1.contains_value(5))


    try:
        m1.add_case(Case(3,1,6))
    except ValueError as e:
        print(f" Erreur Caught : {e}")

    m1.add_case(Case(3,2,3))



    print(m1.get_size())

