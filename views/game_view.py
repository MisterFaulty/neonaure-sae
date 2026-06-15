from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QSpacerItem, QSizePolicy, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QFontMetrics

from .custom_widgets import OutlinedLabel, GrilleWidget

CYAN = "#00CCCC"
WHITE = "#FFFFFF"
GREY = "#C8C8C8"
BLACK = "#000000"

STYLE_ACTION_BTN = f"""
    QPushButton {{
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #40E0D0, stop:1 #00AAAA);
        color: #111;
        border: 1px solid #008888;
        border-radius: 18px;
        padding: 6px 4px;
        font-size: 13px;
        font-weight: bold;
        font-style: italic;
    }}
    QPushButton:hover   {{ background-color: {CYAN}; }}
    QPushButton:pressed {{ background-color: #007777; color: white; }}
"""

STYLE_DIGIT_BTN = f"""
    QPushButton {{
        background-color: #F5F5F5;
        color: #111;
        border: 1px solid {GREY};
        font-family: "Courier New", monospace;
        font-size: 26px;
        font-weight: bold;
    }}
    QPushButton:hover   {{ background-color: #DAEEF0; border: 1px solid {CYAN}; }}
    QPushButton:pressed {{ background-color: {CYAN}; color: white; }}
    QPushButton:checked {{ background-color: {CYAN}; color: white; border: 2px solid #009999; }}
"""


class GameView(QWidget):
    """Vue du jeu, sans logique métier. Émet des signaux pour chaque action."""

    # Signaux émis vers le contrôleur
    digit_selected = pyqtSignal(int)          # pavé numérique
    load_requested = pyqtSignal()
    save_requested = pyqtSignal()
    solve_requested = pyqtSignal()
    hint_requested = pyqtSignal()
    new_requested = pyqtSignal()
    back_requested = pyqtSignal()

    def __init__(self, grille, parent=None):
        super().__init__(parent)
        self.grille_widget = GrilleWidget()
        self.grille_widget.set_grille(grille)

        # Stocke les boutons pour gérer l'état checked
        self.digit_buttons = []
        self.lbl_cell = None

        self._build_ui()
        # Connecte le signal de sélection de case pour afficher les infos
        self.grille_widget.case_selected.connect(self._on_case_selected)

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 15, 0, 15)
        main_layout.setSpacing(0)

        top_line = QFrame()
        top_line.setFrameShape(QFrame.Shape.HLine)
        top_line.setStyleSheet(f"background-color: {CYAN}; max-height: 6px; min-height: 6px; border: none;")
        main_layout.addWidget(top_line)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        content_layout.addWidget(self._grid_container(), stretch=3)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setStyleSheet(f"background-color: {CYAN}; max-width: 3px; min-width: 3px; border: none;")
        content_layout.addWidget(sep)

        content_layout.addWidget(self._side_panel(), stretch=2)

        main_layout.addLayout(content_layout)

        bottom_line = QFrame()
        bottom_line.setFrameShape(QFrame.Shape.HLine)
        bottom_line.setStyleSheet(f"background-color: {CYAN}; max-height: 6px; min-height: 6px; border: none;")
        main_layout.addWidget(bottom_line)

    def _grid_container(self) -> QFrame:
        frame = QFrame()
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        frame.setStyleSheet(f"QFrame {{ background-color: {WHITE}; border: 4px solid {CYAN}; }}")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.grille_widget)
        return frame

    def _side_panel(self) -> QWidget:
        panel = QWidget()
        panel.setFixedWidth(300)
        panel.setStyleSheet(f"background-color: {WHITE}; border: none;")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)

        # Titre
        title_container = QWidget()
        title_vbox = QVBoxLayout(title_container)
        title_vbox.setContentsMargins(0, 0, 0, 0)
        title_vbox.setSpacing(6)
        title_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font_title = QFont("Arial", 32, QFont.Weight.Bold)
        lbl_title = OutlinedLabel("NEONAURE")
        lbl_title.setFont(font_title)
        lbl_title.setFixedHeight(55)
        title_vbox.addWidget(lbl_title)

        fm = QFontMetrics(font_title)
        title_width = fm.horizontalAdvance("NEONAURE")
        double_line = QFrame()
        double_line.setFixedWidth(title_width)
        double_line.setFixedHeight(12)
        double_line.setStyleSheet(f"border-top: 3px solid {CYAN}; border-bottom: 3px solid {CYAN}; background-color: transparent;")
        title_vbox.addWidget(double_line)
        layout.addWidget(title_container)
        layout.addSpacerItem(QSpacerItem(0, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Info case sélectionnée
        layout.addWidget(self._cell_info())

        # Pavé numérique
        digit_container = QWidget()
        digit_layout = QHBoxLayout(digit_container)
        digit_layout.setContentsMargins(0, 0, 0, 0)
        digit_layout.addStretch()
        digit_layout.addWidget(self._digit_pad())
        digit_layout.addStretch()
        layout.addWidget(digit_container)
        layout.addSpacerItem(QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Barres
        line_above = QFrame()
        line_above.setFrameShape(QFrame.Shape.HLine)
        line_above.setStyleSheet(f"background-color: {CYAN}; max-height: 2px; min-height: 2px; border: none;")
        layout.addWidget(line_above)
        layout.addSpacerItem(QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        layout.addWidget(self._action_buttons())
        layout.addSpacerItem(QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        line_below = QFrame()
        line_below.setFrameShape(QFrame.Shape.HLine)
        line_below.setStyleSheet(f"background-color: {CYAN}; max-height: 2px; min-height: 2px; border: none;")
        layout.addWidget(line_below)
        layout.addSpacerItem(QSpacerItem(0, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        layout.addStretch()

        lbl_credits = QLabel("Projet réalisé par Charly Deléglise, Selim Trilla et Younaïs Imamou")
        lbl_credits.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_credits.setWordWrap(True)
        lbl_credits.setStyleSheet("font-size: 9px; color: #444; font-weight: 500;")
        layout.addWidget(lbl_credits)

        return panel

    def _cell_info(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        lbl = QLabel("Case sélectionnée :")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size: 12px; color: #333; font-weight: bold;")

        self.lbl_cell = QLabel("Aucune")
        self.lbl_cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_cell.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        self.lbl_cell.setStyleSheet(f"color: {BLACK};")

        layout.addWidget(lbl)
        layout.addWidget(self.lbl_cell)
        return w

    def _digit_pad(self) -> QWidget:
        w = QWidget()
        main_layout = QVBoxLayout(w)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(12)

        row1_layout = QHBoxLayout()
        row1_layout.setContentsMargins(0, 0, 0, 0)
        row1_layout.setSpacing(12)
        row2_layout = QHBoxLayout()
        row2_layout.setContentsMargins(0, 0, 0, 0)
        row2_layout.setSpacing(12)

        for i in range(1, 4):
            btn = QPushButton(str(i))
            btn.setFixedSize(52, 52)
            btn.setCheckable(True)
            btn.setStyleSheet(STYLE_DIGIT_BTN)
            btn.clicked.connect(self._on_digit_clicked)
            row1_layout.addWidget(btn)
            self.digit_buttons.append(btn)

        row2_layout.addStretch()
        for i in range(4, 6):
            btn = QPushButton(str(i))
            btn.setFixedSize(52, 52)
            btn.setCheckable(True)
            btn.setStyleSheet(STYLE_DIGIT_BTN)
            btn.clicked.connect(self._on_digit_clicked)
            row2_layout.addWidget(btn)
            self.digit_buttons.append(btn)
        row2_layout.addStretch()

        main_layout.addLayout(row1_layout)
        main_layout.addLayout(row2_layout)
        return w

    def _action_buttons(self) -> QWidget:
        w = QWidget()
        grid = QGridLayout(w)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(12)

        actions = [
            ("charger une grille", self.load_requested.emit, 0, 0),
            ("sauvegarder la grille", self.save_requested.emit, 0, 1),
            ("résoudre la grille", self.solve_requested.emit, 1, 0),
            ("avoir un indice", self.hint_requested.emit, 1, 1),
            ("nouvelle grille", self.new_requested.emit, 2, 0),
            ("menu principal", self.back_requested.emit, 2, 1),
        ]

        for label, slot, row, col in actions:
            btn = QPushButton(label)
            btn.setFixedHeight(36)
            btn.setStyleSheet(STYLE_ACTION_BTN)
            btn.clicked.connect(slot)
            grid.addWidget(btn, row, col)

        return w

    # --- Gestion des entrées utilisateur (émet uniquement des signaux) ---

    def _on_digit_clicked(self):
        sender = self.sender()
        for btn in self.digit_buttons:
            if btn is not sender:
                btn.setChecked(False)

        if sender.isChecked():
            value = int(sender.text())
            self.digit_selected.emit(value)
        else:
            sender.setChecked(False)

    def _on_case_selected(self, case_ihm):
        """Met à jour l'affichage de la case sélectionnée (pas de logique métier)."""
        if case_ihm:
            case = case_ihm.case
            self.lbl_cell.setText(f"L{case.get_y()+1} C{case.get_x()+1}")
        else:
            self.lbl_cell.setText("aucune")

    # --- Méthodes publiques pour le contrôleur ---

    def set_cell_info(self, case_ihm):
        """Appelé par le contrôleur après un mouvement pour rafraîchir l'info."""
        self._on_case_selected(case_ihm)

    def set_grille(self, grille):
        self.grille_widget.set_grille(grille)

    def refresh_grid(self):
        self.grille_widget.refresh_all()

    def update_cell_after_move(self, x, y, is_error):
        """Met à jour visuellement une cellule après un placement."""
        self.grille_widget.update_cell(x, y, self.grille_widget.grille.get_case(x, y).get_value(), is_error)

    def check_victory(self):
        return self.grille_widget.check_victory()

    def keyPressEvent(self, event):
        event.ignore()