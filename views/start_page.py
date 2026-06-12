# views/start_page.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QSpacerItem, QSizePolicy, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QFontMetrics

from .custom_widgets import OutlinedLabel

CYAN = "#00CCCC"
WHITE = "#FFFFFF"
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


class StartPage(QWidget):
    new_grid_requested = pyqtSignal()
    load_grid_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {WHITE};")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(0)
        layout.addStretch(2)

        font_title = QFont("Arial", 64, QFont.Weight.Bold)
        title = OutlinedLabel("NEONAURE")
        title.outline_width = 5
        title.setFont(font_title)
        title.setFixedHeight(110)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        fm = QFontMetrics(font_title)
        title_width = fm.horizontalAdvance("NEONAURE")
        double_line = QFrame()
        double_line.setFixedWidth(title_width)
        double_line.setFixedHeight(16)
        double_line.setStyleSheet(
            f"border-top: 4px solid {CYAN}; border-bottom: 4px solid {CYAN}; background-color: transparent;"
        )

        line_row = QHBoxLayout()
        line_row.addStretch()
        line_row.addWidget(double_line)
        line_row.addStretch()
        layout.addLayout(line_row)

        layout.addSpacerItem(QSpacerItem(0, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        self.btn_new = QPushButton("nouvelle grille aléatoire")
        self.btn_load = QPushButton("charger une grille")
        for btn in (self.btn_new, self.btn_load):
            btn.setFixedSize(320, 50)
            btn.setStyleSheet(STYLE_ACTION_BTN)
            row = QHBoxLayout()
            row.addStretch()
            row.addWidget(btn)
            row.addStretch()
            layout.addLayout(row)
            layout.addSpacerItem(QSpacerItem(0, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        self.btn_new.clicked.connect(self.new_grid_requested.emit)
        self.btn_load.clicked.connect(self.load_grid_requested.emit)

        layout.addStretch(3)

        lbl_credits = QLabel("Projet réalisé par Charly Deléglise, Selim Trilla et Younaïs Imamou")
        lbl_credits.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_credits.setStyleSheet("font-size: 9px; color: #444; font-weight: 500;")
        layout.addWidget(lbl_credits)