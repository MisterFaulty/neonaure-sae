# controllers/game_controller.py
from PyQt6.QtWidgets import QMessageBox, QFileDialog, QApplication
from PyQt6.QtCore import QObject, Qt
from modele.Grille import Grille
from modele.Validator import Validator
from modele.Solver import Solver
from views.game_view import GameView
import os


class GameController(QObject):
    """Contrôleur qui gère la logique du jeu, fait le lien entre la vue et le modèle."""

    back_to_menu = None  # signal émis par la fenêtre principale, on le redirige

    def __init__(self, parent=None):
        super().__init__(parent)
        self.grille = Grille(8, 8)
        self.view = GameView(self.grille)

        # Connexion des signaux de la vue aux slots du contrôleur
        self.view.digit_selected.connect(self.on_digit_clicked)
        self.view.load_requested.connect(self.on_load)
        self.view.save_requested.connect(self.on_save)
        self.view.solve_requested.connect(self.on_solve)
        self.view.hint_requested.connect(self.on_hint)
        self.view.new_requested.connect(self.on_new)
        self.view.back_requested.connect(self.on_back)

    def set_back_callback(self, callback):
        """Méthode pour transmettre le signal de retour au menu depuis l'extérieur."""
        self.back_to_menu = callback

    def on_digit_clicked(self, value):
        case_ihm = self.view.grille_widget.get_selected_case()
        if case_ihm is None:
            return
        case = case_ihm.case
        if case.is_hint():
            return

        x, y = case.get_x(), case.get_y()
        if value == 0:
            case.set_value(0)
            self.view.update_cell_after_move(x, y, False)
        else:
            is_valid, _ = Validator.check_move(self.grille, x, y, value)
            case.set_value(value)
            self.view.update_cell_after_move(x, y, not is_valid)

        # Mise à jour de l'info de la case sélectionnée
        self.view.set_cell_info(case_ihm)
        self._check_victory()

    def on_load(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "charger une grille", "",
                                                   "fichiers JSON (*.json);;tous les fichiers (*)")
        if file_path:
            try:
                grille = Grille()
                grille.load_json(file_path)
                self.grille = grille
                self.view.set_grille(self.grille)
                QMessageBox.information(self.view, "chargement", f"grille chargée depuis {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self.view, "erreur", f"impossible de charger la grille :\n{e}")

    def on_save(self):
        file_path, _ = QFileDialog.getSaveFileName(self.view, "sauvegarder la grille", "grille.json",
                                                   "fichiers JSON (*.json);;tous les fichiers (*)")
        if file_path:
            try:
                self.grille.save_json(file_path)
                QMessageBox.information(self.view, "sauvegarde", f"grille sauvegardée dans {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self.view, "erreur", f"impossible de sauvegarder la grille :\n{e}")

    def on_solve(self):
        reply = QMessageBox.question(self.view, "résoudre", "voulez vous avoir la solution de la grille ?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if Solver.solve(self.grille):
                self.view.refresh_grid()
                QMessageBox.information(self.view, "résolution", "grille résolue !!")
            else:
                QMessageBox.warning(self.view, "résolution", "impossible de résoudre cette grille")

    def on_hint(self):
        result = Solver.get_hint(self.grille)
        if result:
            x, y, value = result
            case = self.grille.get_case(x, y)
            case.set_value(value)
            self.view.refresh_grid()
            QMessageBox.information(self.view, "indice", f"case L{y+1} C{x+1} = {value}")
        else:
            QMessageBox.warning(self.view, "indice", "aucun indice dispo :(")

    def generate_new_grid(self):
        """Génère une nouvelle grille sans demander de confirmation."""
        self.grille = Grille(8, 8)
        self.grille.generate_motifs(min_size=2, max_size=5, hint_chance=0.25)
        self.view.set_grille(self.grille)

    def on_new(self):
        reply = QMessageBox.question(self.view, "nouvelle grille",
                                     "Voulez vous générer une nouvelle grille ? L'ancienne sera perdue si non sauvegardée",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.generate_new_grid()
            self.grille = Grille(8, 8)
            self.grille.generate_motifs(min_size=2, max_size=5, hint_chance=0.25)
            self.view.set_grille(self.grille)
            QMessageBox.information(self.view, "nouvelle grille", "nouvelle grille générée !")

    def on_back(self):
        if self.back_to_menu:
            self.back_to_menu()

    def _check_victory(self):
        is_complete, _ = self.view.check_victory()
        if is_complete:
            QMessageBox.information(self.view, "bravo! !", "vous avez résolu la grille !!!! :)")

    def key_press_handler(self, event):
        """Gère les touches clavier pour placer des chiffres ou effacer."""
        text = event.text()
        if text.isdigit() and "1" <= text <= "5":
            self.on_digit_clicked(int(text))
        elif event.key() in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete, Qt.Key.Key_0):
            self.on_digit_clicked(0)