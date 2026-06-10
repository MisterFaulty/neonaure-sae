# Première version du style de l'interface du Neonaure
# par Charly Deléglise
# --------------------------------------------------------------------------------------------------------------- #

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QGridLayout, QFrame, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor, QPainter, QPainterPath, QPen, QBrush, QFontMetrics

# --------------------------------------------------------------------------------------------------------------- #

# les couleurs
CYAN       = "#00CCCC"
DARK_CYAN  = "#009999"
WHITE      = "#FFFFFF"
LIGHT_GREY = "#F5F5F5"
GREY       = "#C8C8C8"
BLACK      = "#000000"

# boutons style windows7
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

# pavé numérique
STYLE_DIGIT_BTN = f"""
    QPushButton {{
        background-color: {LIGHT_GREY};
        color: #111;
        border: 1px solid {GREY};
        font-family: "Courier New", monospace;
        font-size: 26px;
        font-weight: bold;
    }}
    QPushButton:hover   {{ background-color: #DAEEF0; border: 1px solid {CYAN}; }}
    QPushButton:pressed {{ background-color: {CYAN}; color: white; }}
    QPushButton:checked {{ background-color: {CYAN}; color: white; border: 2px solid {DARK_CYAN}; }}
"""

# --------------------------------------------------------------------------------------------------------------- #

class OutlinedLabel(QLabel):
    # widget pour text blanc contour cyan
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.outline_color = QColor(CYAN)
        self.fill_color = QColor(WHITE)
        self.outline_width = 3

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        font = self.font()
        fm = QFontMetrics(font)
        
        text = self.text()
        text_width = fm.horizontalAdvance(text)
        
        # calcul du centrage
        x = (rect.width() - text_width) // 2
        y = (rect.height() + fm.ascent() - fm.descent()) // 2
        
        path = QPainterPath()
        path.addText(x, y, font, text)
        
        # correction de l'attribut : PenCapStyle.RoundCap
        pen = QPen(self.outline_color, self.outline_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawPath(path)
        
        painter.fillPath(path, QBrush(self.fill_color))

# --------------------------------------------------------------------------------------------------------------- #

# la fenètre !!
class NeonaurWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neonaure")
        self.setMinimumSize(780, 585)
        self.resize(780, 585)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(WHITE))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self._build_ui()

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)

        main_layout = QVBoxLayout(root)
        main_layout.setContentsMargins(0, 15, 0, 15)
        main_layout.setSpacing(0)

        # ligne cyan supérieure
        top_line = QFrame()
        top_line.setFrameShape(QFrame.Shape.HLine)
        top_line.setStyleSheet(f"background-color: {CYAN}; max-height: 6px; min-height: 6px; border: none;")
        main_layout.addWidget(top_line)

        # conteneur central
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        content_layout.addWidget(self._grid_placeholder(), stretch=3)

        # ligne de séparation centrale verticale
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setStyleSheet(f"background-color: {CYAN}; max-width: 3px; min-width: 3px; border: none;")
        content_layout.addWidget(sep)

        content_layout.addWidget(self._side_panel(), stretch=2)

        main_layout.addLayout(content_layout)

        # ligne cyan inférieure
        bottom_line = QFrame()
        bottom_line.setFrameShape(QFrame.Shape.HLine)
        bottom_line.setStyleSheet(f"background-color: {CYAN}; max-height: 6px; min-height: 6px; border: none;")
        main_layout.addWidget(bottom_line)

    def _grid_placeholder(self) -> QFrame:
        frame = QFrame()
        frame.setMinimumSize(400, 400)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        frame.setStyleSheet(f"QFrame {{ background-color: {WHITE}; border: 4px solid {CYAN}; }}")

        layout = QVBoxLayout(frame)
        lbl = QLabel("Je suis une grille ^^")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet(f"color: {BLACK}; font-size: 16px; border: none;")
        layout.addWidget(lbl)

        return frame

    def _side_panel(self) -> QWidget:
        panel = QWidget()
        panel.setFixedWidth(300) 
        panel.setStyleSheet(f"background-color: {WHITE}; border: none;")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        # conteneur pour l'alignement et le soulignement propre
        title_container = QWidget()
        title_vbox = QVBoxLayout(title_container)
        title_vbox.setContentsMargins(0, 0, 0, 0)
        title_vbox.setSpacing(6)
        title_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # grand titre
        font_title = QFont("Arial", 32, QFont.Weight.Bold)
        self.lbl_title = OutlinedLabel("NEONAURE")
        self.lbl_title.setFont(font_title)
        self.lbl_title.setFixedHeight(55)
        title_vbox.addWidget(self.lbl_title)
        fm = QFontMetrics(font_title)
        title_width = fm.horizontalAdvance("NEONAURE")

        # le soulignement (en double!!)
        double_line = QFrame()
        double_line.setFixedWidth(title_width)
        double_line.setFixedHeight(12)
        double_line.setStyleSheet(f"border-top: 3px solid {CYAN}; border-bottom: 3px solid {CYAN}; background-color: transparent;")
        title_vbox.addWidget(double_line)

        layout.addWidget(title_container)

        layout.addSpacerItem(QSpacerItem(0, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        layout.addWidget(self._cell_info())

        layout.addSpacerItem(QSpacerItem(0, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # zone du pavé numérique propre
        digit_container = QWidget()
        digit_layout = QHBoxLayout(digit_container)
        digit_layout.setContentsMargins(0, 0, 0, 0)
        digit_layout.addStretch()
        digit_layout.addWidget(self._digit_pad())
        digit_layout.addStretch()
        layout.addWidget(digit_container)

        layout.addSpacerItem(QSpacerItem(0, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        
        # lignes de séparations horizontales au dessus et en dessous des boutons d'action
        line_above = QFrame()
        line_above.setFrameShape(QFrame.Shape.HLine)
        line_above.setStyleSheet(f"background-color: {CYAN}; max-height: 2px; min-height: 2px; border: none;")
        layout.addWidget(line_above)
        layout.addSpacerItem(QSpacerItem(0, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        layout.addWidget(self._action_buttons())
        layout.addSpacerItem(QSpacerItem(0, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        line_below = QFrame()
        line_below.setFrameShape(QFrame.Shape.HLine)
        line_below.setStyleSheet(f"background-color: {CYAN}; max-height: 2px; min-height: 2px; border: none;")
        layout.addWidget(line_below)
        layout.addSpacerItem(QSpacerItem(0, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        layout.addStretch()

        # signature
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

        lbl = QLabel("Case cliquée :")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size: 12px; color: #333; font-weight: bold;")

        self.lbl_cell = QLabel("L? C?")
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

        # boutons 1, 2, 3
        row1_layout = QHBoxLayout()
        row1_layout.setContentsMargins(0, 0, 0, 0)
        row1_layout.setSpacing(12)

        # boutons 4, 5
        row2_layout = QHBoxLayout()
        row2_layout.setContentsMargins(0, 0, 0, 0)
        row2_layout.setSpacing(12)

        self.digit_buttons: list[QPushButton] = []
        
        # ajout des boutons 1 à 3 sur la première ligne
        for i in range(1, 4):
            btn = QPushButton(str(i))
            btn.setFixedSize(52, 52)
            btn.setCheckable(True)
            btn.setStyleSheet(STYLE_DIGIT_BTN)
            btn.clicked.connect(self._on_digit_clicked)
            row1_layout.addWidget(btn)
            self.digit_buttons.append(btn)

        # ajout des boutons 4 et 5 propre en dessous (5 cases pas 6 comme la maquette!!)
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
            ("charger une grille",     self._on_load,  0, 0),
            ("sauvegarder la grille",  self._on_save,  0, 1),
            ("résoudre la grille",     self._on_solve, 1, 0),
            ("avoir un indice",        self._on_hint,  1, 1),
        ]

        for label, slot, row, col in actions:
            btn = QPushButton(label)
            btn.setFixedHeight(36)
            btn.setStyleSheet(STYLE_ACTION_BTN)
            btn.clicked.connect(slot)
            grid.addWidget(btn, row, col)

        return w

    # test des boutons pour accorder avec les classes des copains
    def _on_digit_clicked(self):
        for btn in self.digit_buttons:
            if btn is not self.sender():
                btn.setChecked(False)

    def _on_load(self):  print("test charger ok")
    def _on_save(self):  print("test sauvegarder ok")
    def _on_solve(self): print("test résoudre ok")
    def _on_hint(self):  print("test indice ok")

# --------------------------------------------------------------------------------------------------------------- #

# un main parcequ'il faut un main...
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = NeonaurWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

# si tu vois ça dans le git c'est que le push a bien marché et que tu as la dernère version de "interfacev1.py"!! :)