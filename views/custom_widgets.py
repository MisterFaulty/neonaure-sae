from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPainter, QPainterPath, QPen, QBrush, QFontMetrics, QColor

from modele.Case import Case
from modele.Motif import Motif
from modele.Grille import Grille
from modele.Validator import Validator

CYAN = "#00CCCC"
DARK_CYAN = "#009999"
WHITE = "#FFFFFF"
LIGHT_GREY = "#F5F5F5"
GREY = "#C8C8C8"
BLACK = "#000000"
ERROR_RED = "#FF6B6B"
HINT_BLUE = "#4A90D9"


class OutlinedLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.outline_color = CYAN
        self.fill_color = WHITE
        self.outline_width = 3

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        font = self.font()
        fm = QFontMetrics(font)

        text = self.text()
        text_width = fm.horizontalAdvance(text)

        x = (rect.width() - text_width) // 2
        y = (rect.height() + fm.ascent() - fm.descent()) // 2

        path = QPainterPath()
        path.addText(x, y, font, text)

        pen = QPen(QColor(self.outline_color), self.outline_width, Qt.PenStyle.SolidLine,
                   Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawPath(path)

        painter.fillPath(path, QBrush(QColor(self.fill_color)))


class CaseIHM(QLabel):
    clicked = pyqtSignal(object)

    def __init__(self, case, parent=None):
        super().__init__(parent)
        self.case = case
        self.bordures = []
        self.is_error = False

        self.setMinimumSize(20, 20)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.update_display()

    def set_bordures(self, bordures):
        self.bordures = bordures
        self.update_style(False)

    def update_style(self, selectionnee=False):
        b_top = f"3px solid {CYAN}" if "top" in self.bordures else f"1px solid {GREY}"
        b_bottom = f"3px solid {CYAN}" if "bottom" in self.bordures else f"1px solid {GREY}"
        b_left = f"3px solid {CYAN}" if "left" in self.bordures else f"1px solid {GREY}"
        b_right = f"3px solid {CYAN}" if "right" in self.bordures else f"1px solid {GREY}"

        if self.is_error:
            bg_color = ERROR_RED
        elif selectionnee:
            bg_color = "#DDEEFF"
        else:
            bg_color = WHITE

        text_color = HINT_BLUE if self.case.is_hint() else "#2c3e50"

        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                border-top: {b_top};
                border-bottom: {b_bottom};
                border-left: {b_left};
                border-right: {b_right};
                color: {text_color};
            }}
        """)

    def update_display(self):
        val = self.case.get_value()
        self.setText(str(val) if val > 0 else "")

    def set_error(self, is_error):
        self.is_error = is_error

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = self.width()
        h = self.height()
        font_size = max(10, min(w, h) // 2)
        font = QFont("Arial", font_size, QFont.Weight.Bold)
        self.setFont(font)


class GrilleWidget(QWidget):
    case_selected = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.grille = None
        self.cases_ihm = {}
        self.case_selectionnee = None
        self.layout_grille = QGridLayout(self)
        self.layout_grille.setSpacing(0)
        self.layout_grille.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_grille(self, grille):
        self.grille = grille
        self.case_selectionnee = None
        self._build_grid()

    def _build_grid(self):
        # Nettoyage
        while self.layout_grille.count():
            item = self.layout_grille.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.cases_ihm = {}
        if self.grille is None:
            return

        width = self.grille.get_width()
        height = self.grille.get_height()

        for i in range(width):
            self.layout_grille.setColumnStretch(i, 1)
        for i in range(height):
            self.layout_grille.setRowStretch(i, 1)

        for y in range(height):
            for x in range(width):
                case = self.grille.get_case(x, y)
                if case is None:
                    continue
                case_ihm = CaseIHM(case)
                case_ihm.clicked.connect(self._on_case_clicked)
                bordures = self._calculate_borders(x, y)
                case_ihm.set_bordures(bordures)
                self.layout_grille.addWidget(case_ihm, y, x)
                self.cases_ihm[(x, y)] = case_ihm

    def _calculate_borders(self, x, y):
        bordures = []
        motif = self.grille.get_motif_of(x, y)
        if motif is None:
            return bordures

        if y == 0 or self.grille.get_motif_of(x, y - 1) != motif:
            bordures.append("top")
        if y == self.grille.get_height() - 1 or self.grille.get_motif_of(x, y + 1) != motif:
            bordures.append("bottom")
        if x == 0 or self.grille.get_motif_of(x - 1, y) != motif:
            bordures.append("left")
        if x == self.grille.get_width() - 1 or self.grille.get_motif_of(x + 1, y) != motif:
            bordures.append("right")
        return bordures

    def _on_case_clicked(self, case_ihm):
        if self.case_selectionnee:
            self.case_selectionnee.update_style(False)
        self.case_selectionnee = case_ihm
        self.case_selectionnee.update_style(True)
        self.case_selected.emit(case_ihm)

    def get_selected_case(self):
        return self.case_selectionnee

    def update_cell(self, x, y, value, is_error):
        """Met à jour l'affichage d'une cellule après un mouvement."""
        case_ihm = self.cases_ihm.get((x, y))
        if case_ihm:
            case_ihm.set_error(is_error)
            case_ihm.update_display()
            if self.case_selectionnee == case_ihm:
                case_ihm.update_style(True)

    def refresh_all(self):
        for case_ihm in self.cases_ihm.values():
            case_ihm.update_display()
            case_ihm.set_error(False)
            if case_ihm == self.case_selectionnee:
                case_ihm.update_style(True)
            else:
                case_ihm.update_style(False)

    def check_victory(self):
        return Validator.check_grid_complete(self.grille)