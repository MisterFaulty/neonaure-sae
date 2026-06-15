from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from views.start_page import StartPage
from controllers.game_controller import GameController
import os
 
WHITE = "#FFFFFF"
 
 
class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neonaure")
        self.setMinimumSize(825, 550)
        self.resize(825, 550)
 
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(WHITE))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
 
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
 
        self.start_page = StartPage()
        self.stack.addWidget(self.start_page)
 
        self.game_controller = None
        self.game_page = None
 
        self.start_page.new_grid_requested.connect(self._on_new_grid)
        self.start_page.load_grid_requested.connect(self._on_load_grid)
        self.stack.setCurrentWidget(self.start_page)
 
    def _init_game(self):
        """Crée le contrôleur de jeu s'il n'existe pas encore."""
        if self.game_controller is None:
            self.game_controller = GameController()
            self.game_controller.set_back_callback(self._on_back_to_menu)
            self.game_page = self.game_controller.view
            self.stack.addWidget(self.game_page)
 
    def _on_new_grid(self):
        self._init_game()
        self.game_controller.generate_new_grid()  # pas de dialog de confirmation
        self.stack.setCurrentWidget(self.game_page)
 
    def _on_load_grid(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "charger une grille", "",
                                                   "fichiers JSON (*.json);;tous les fichiers (*)")
        if file_path:
            self._init_game()
            if self.game_controller.load_grid(file_path):
                self.stack.setCurrentWidget(self.game_page)
                QMessageBox.information(self, "chargement",
                                        f"grille chargée depuis {os.path.basename(file_path)}")
            else:
                QMessageBox.critical(self, "erreur", "impossible de charger la grille")
 
    def _on_back_to_menu(self):
        self.stack.setCurrentWidget(self.start_page)
 
    def keyPressEvent(self, event):
        if self.stack.currentWidget() is self.game_page and self.game_controller:
            self.game_controller.key_press_handler(event)
        else:
            super().keyPressEvent(event)