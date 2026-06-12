"""Creation de la classe Case du jeu Neonaure.

Une Case est la brique élémentaire de la grille de jeu : elle porte
des coordonnées (x, y) et une valeur (0 si vide, 1 à 5 sinon).
"""
class Case:
    """Represente  une case de la grille du jeu.

        Attributes:
            x (int): Coordonnée horizontale (en lecture seule).
            y (int): Coordonnée verticale (en lecture seule).
            value (int): Valeur affichée dans la case, 0 si vide.
        """

    def __init__(self,x,y,value=0):
        """Initialise une case avec ses coordonnées et sa valeur.

               Args:
               x (int): Coordonnée horizontale.
               y (int): Coordonnée verticale.
               value (int, optionnel): Valeur initiale (0 par défaut, case vide).
        """

        self.__x = x
        self.__y = y
        self.set_value(value)

    """
    Creation des getters/setters pour x ,y et valeur
    
    """
    #  ---  Getters  ---
    def get_x(self):
        """Retourne la coordonnée x de la case."""
        return self.__x


    def get_y(self):
        """Retourne la coordonnée y de la case."""
        return self.__y


    def get_value(self):
        """Retourne la valeur actuelle de la case (0 si vide)."""
        return self.__value


    # --- Setters ---

    def set_value(self,value):
        """
        Param:
            value (int): Nouvelle valeur, doit être entre 0 et 5 inclus.

         Raises:
            ValueError: Si la valeur n'est pas dans l'intervalle [0, 5].
        """



        if value < 0 or value> 5:
            raise ValueError("value must be between 0 and 5")
        self.__value = value

    # Affichage simple

    def __str__(self):
        """Retourne une représentation lisible de la case."""
        return f"Case({self.get_x()},{self.get_y()},{self.get_value()})"


# --- Test ---
if __name__ == "__main__":
    c1= Case(1,2,3)
    c2 =Case(0,0,0)
    c3 = Case(1,3,2)



    print(c1)
    print("\n")
    print(c2)

    print("Les coordonnes de c1  :",c1.get_x(),c1.get_y())
    print("Valeur de c1 :",c1.get_value())

    print("\n")

    print("les coordonnes de c2  :",c2.get_x(),c2.get_y())
    print("Le valeur de c2 :",c2.get_value())


    c2.set_value(5)
    print("\n")
    print("Après modification :", c2)


#Je m'amuse avec try and catch et je verifie aussi les erreurs
    try:
        c3.set_value(7)
    except ValueError as e:
        print(f"Caught error: {e}")

    try:
        c3.set_value(-1)
    except ValueError as e:
        print(f"Caught error: {e}")
    try:
        c3.set_value(5)
        print(f"Accepted Value: {c3.get_value()}")
    except ValueError as e:
            print(f"Caught error: {e}")