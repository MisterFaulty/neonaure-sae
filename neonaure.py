# neonaure.py
# le fichier relie le code de plusieurs autres fichiers du git
# l'affichage et le style sont quasi parfait
# le générateur de grille et le solver ont quelques problèmes
# fichier """final""" à revoir côté algo
# --------------------------------------------------------------------------------------------------------------- #

import sys
import json
import random
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QGridLayout, QFrame, QSizePolicy, QSpacerItem,
    QFileDialog, QMessageBox, QStackedWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor, QPainter, QPainterPath, QPen, QBrush, QFontMetrics, QResizeEvent

# == Classes ========================================================================================================== #

class Case:

    def __init__(self, x, y, value=0):
        self.__x = x
        self.__y = y
        self.__value = 0
        self.__is_hint = False
        self.set_value(value)

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_value(self):
        return self.__value

    def is_hint(self):
        return self.__is_hint

    def set_hint(self, is_hint):
        self.__is_hint = is_hint

    def set_value(self, value):
        if value < 0 or value > 5:
            raise ValueError("La valeur doit être entre 0 et 5")
        self.__value = value

    def __str__(self):
        return f"Case({self.__x},{self.__y},{self.__value})"


class Motif:
    MAX_SIZE = 5

    def __init__(self, name):
        self.__name = name
        self.__cases = []

    def get_name(self):
        return self.__name

    def get_cases(self):
        return self.__cases

    def get_size(self):
        return len(self.__cases)

    def add_case(self, case):
        if self.get_size() >= Motif.MAX_SIZE:
            raise ValueError(f"Un motif ne peut pas dépasser {Motif.MAX_SIZE} cases")
        self.__cases.append(case)

    def contains(self, x, y):
        for case in self.__cases:
            if case.get_x() == x and case.get_y() == y:
                return True
        return False

    def contains_value(self, value):
        for case in self.__cases:
            if case.get_value() == value:
                return True
        return False

    def __str__(self):
        cases_str = ", ".join(str(c) for c in self.__cases)
        return f"Motif({self.__name}, {self.get_size()} cases): [{cases_str}]"


class Grille:
    def __init__(self, width=8, height=8):
        self.__height = height
        self.__width = width
        self.__cases_by_pos = {}
        self.__cases = []
        self.__motifs = []
        self.__generate_empty()

    def __generate_empty(self):
        for y in range(self.__height):
            for x in range(self.__width):
                case = Case(x, y, 0)
                self.__cases.append(case)
                self.__cases_by_pos[(x, y)] = case

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_cases(self):
        return self.__cases

    def get_motifs(self):
        return self.__motifs

    def get_case(self, x, y):
        return self.__cases_by_pos.get((x, y))

    def get_motif_of(self, x, y):
        for motif in self.__motifs:
            if motif.contains(x, y):
                return motif
        return None

    def add_motif(self, motif):
        self.__motifs.append(motif)
        for case in motif.get_cases():
            existing = self.get_case(case.get_x(), case.get_y())
            if existing is None:
                self.__cases.append(case)
                self.__cases_by_pos[(case.get_x(), case.get_y())] = case

    def generate_motifs(self, min_size=2, max_size=5, hint_chance=0.25):
        min_size = max(1, min(min_size, Motif.MAX_SIZE))
        max_size = max(min_size, min(max_size, Motif.MAX_SIZE))

        self.__motifs = []
        for case in self.__cases:
            case.set_value(0)
            case.set_hint(False)

        visited = [[False] * self.__height for _ in range(self.__width)]
        motif_index = 1

        for x in range(self.__width):
            for y in range(self.__height):
                if visited[x][y]:
                    continue

                motif = Motif(f"motif{motif_index}")
                motif_index += 1
                target_size = random.randint(min_size, max_size)

                queue = [(x, y)]
                while queue and motif.get_size() < target_size:
                    idx = random.randint(0, len(queue) - 1)
                    cx, cy = queue.pop(idx)
                    if cx < 0 or cx >= self.__width or cy < 0 or cy >= self.__height:
                        continue
                    if visited[cx][cy]:
                        continue

                    visited[cx][cy] = True
                    case = self.get_case(cx, cy)
                    if case is None:
                        case = Case(cx, cy, 0)
                        self.__cases.append(case)
                        self.__cases_by_pos[(cx, cy)] = case
                    motif.add_case(case)

                    neighbours = [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]
                    random.shuffle(neighbours)
                    for nx, ny in neighbours:
                        if 0 <= nx < self.__width and 0 <= ny < self.__height and not visited[nx][ny]:
                            queue.append((nx, ny))

                size = motif.get_size()
                max_hint = min(size, 5)
                for case in motif.get_cases():
                    if max_hint > 0 and random.random() < hint_chance:
                        val = random.randint(1, max_hint)
                        case.set_value(val)
                        case.set_hint(True)

                self.__motifs.append(motif)

    def load_json(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.__cases_by_pos = {}
        self.__cases = []
        self.__motifs = []
        max_x, max_y = 0, 0

        for name, cells in data.items():
            motif = Motif(name)
            for cell in cells:
                x, y, value = cell[0], cell[1], cell[2]
                case = Case(x, y, value)
                if value != 0:
                    case.set_hint(True)
                motif.add_case(case)
                self.__cases.append(case)
                self.__cases_by_pos[(x, y)] = case
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
            self.__motifs.append(motif)

        self.__width = max_x + 1
        self.__height = max_y + 1

    def save_json(self, file_path):
        data = {}
        for motif in self.__motifs:
            cells = []
            for case in motif.get_cases():
                cells.append([case.get_x(), case.get_y(), case.get_value()])
            data[motif.get_name()] = cells

        lines = []
        for name, cells in data.items():
            cells_str = ", ".join(f"[{c[0]},{c[1]},{c[2]}]" for c in cells)
            lines.append(f'  "{name}": [{cells_str}]')

        json_content = "{\n" + ",\n".join(lines) + "\n}"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json_content)

    def to_dict(self):
        data = {}
        for motif in self.__motifs:
            cells = []
            for case in motif.get_cases():
                cells.append([case.get_x(), case.get_y(), case.get_value()])
            data[motif.get_name()] = cells
        return data

    def __str__(self):
        lines = [f"Grille {self.__width} x {self.__height}:"]
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                case = self.get_case(x, y)
                if case is None:
                    row.append(".")
                else:
                    v = case.get_value()
                    row.append(str(v) if v != 0 else "·")
            lines.append(" ".join(row))
        return "\n".join(lines)


class Validator:
    @staticmethod
    def check_move(grid, x, y, value):
        if not (1 <= value <= 5):
            return False, "La valeur doit être entre 1 et 5."

        motif = grid.get_motif_of(x, y)
        if motif is None:
            return False, "La case n'appartient à aucun motif."

        motif_cells = motif.get_cases()
        motif_size = len(motif_cells)

        if value > motif_size:
            return False, f"Motif de taille {motif_size}, valeur max autorisée : {motif_size}."

        for cell in motif_cells:
            if cell.get_x() == x and cell.get_y() == y:
                continue
            if cell.get_value() == value:
                return False, f"La valeur {value} est déjà présente dans ce motif."

        is_valid, message = Validator._check_neighbors(grid, x, y, value)
        if not is_valid:
            return False, message

        return True, "Coup valide."

    @staticmethod
    def _check_neighbors(grid, x, y, value):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor = grid.get_case(x + dx, y + dy)
                if neighbor is not None and neighbor.get_value() == value:
                    return False, f"La valeur {value} touche un voisin identique."
        return True, ""

    @staticmethod
    def check_grid_complete(grid):
        for cell in grid.get_cases():
            if cell.get_value() == 0:
                return False, "Grille incomplète."
            is_valid, msg = Validator.check_move(grid, cell.get_x(), cell.get_y(), cell.get_value())
            if not is_valid:
                return False, f"Conflit en ({cell.get_x()},{cell.get_y()}): {msg}"
        return True, "Grille parfaite !"


class Solver:
    @staticmethod
    def solve(grid):
        empty_cell = Solver.find_empty_cell(grid)
        if empty_cell is None:
            return True

        x = empty_cell.get_x()
        y = empty_cell.get_y()

        for value in range(1, 6):
            is_valid, _ = Validator.check_move(grid, x, y, value)
            if is_valid:
                empty_cell.set_value(value)
                if Solver.solve(grid):
                    return True
                empty_cell.set_value(0)

        return False

    @staticmethod
    def find_empty_cell(grid):
        for case in grid.get_cases():
            if case.get_value() == 0:
                return case
        return None

    @staticmethod
    def get_hint(grid):
        original_values = {}
        for case in grid.get_cases():
            original_values[(case.get_x(), case.get_y())] = case.get_value()

        if Solver.solve(grid):
            for (x, y), orig_val in original_values.items():
                if orig_val == 0:
                    case = grid.get_case(x, y)
                    hint_value = case.get_value()
                    for (rx, ry), rv in original_values.items():
                        grid.get_case(rx, ry).set_value(rv)
                    return x, y, hint_value

        for (x, y), v in original_values.items():
            grid.get_case(x, y).set_value(v)
        return None


# == Vue ============================================================================================================= #

CYAN = "#00CCCC"
DARK_CYAN = "#009999"
WHITE = "#FFFFFF"
LIGHT_GREY = "#F5F5F5"
GREY = "#C8C8C8"
BLACK = "#000000"
ERROR_RED = "#FF6B6B"
HINT_BLUE = "#4A90D9"

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


class OutlinedLabel(QLabel):
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

        x = (rect.width() - text_width) // 2
        y = (rect.height() + fm.ascent() - fm.descent()) // 2

        path = QPainterPath()
        path.addText(x, y, font, text)

        pen = QPen(self.outline_color, self.outline_width, Qt.PenStyle.SolidLine,
                   Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawPath(path)

        painter.fillPath(path, QBrush(self.fill_color))


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

        if y == 0 or self.grille.get_motif_of(x, y-1) != motif:
            bordures.append("top")
        if y == self.grille.get_height()-1 or self.grille.get_motif_of(x, y+1) != motif:
            bordures.append("bottom")
        if x == 0 or self.grille.get_motif_of(x-1, y) != motif:
            bordures.append("left")
        if x == self.grille.get_width()-1 or self.grille.get_motif_of(x+1, y) != motif:
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

    def set_value(self, value):
        if self.case_selectionnee is None:
            return False, ""

        case = self.case_selectionnee.case
        if case.is_hint():
            return False, ""

        x, y = case.get_x(), case.get_y()

        if value == 0:
            case.set_value(0)
            self.case_selectionnee.set_error(False)
            self.case_selectionnee.update_display()
            self.case_selectionnee.update_style(True)
            return True, ""

        is_valid, _ = Validator.check_move(self.grille, x, y, value)
        case.set_value(value)
        self.case_selectionnee.set_error(not is_valid)
        self.case_selectionnee.update_display()
        self.case_selectionnee.update_style(True)
        return is_valid, ""

    def refresh_all(self):
        for case_ihm in self.cases_ihm.values():
            case_ihm.update_display()
            case_ihm.set_error(False)
            case_ihm.update_style(case_ihm == self.case_selectionnee)

    def check_victory(self):
        return Validator.check_grid_complete(self.grille)


# == Page d'accueil =================================================================================================== #

class StartPage(QWidget):
    """Page d'entrée du jeu : titre + choix nouvelle grille / chargement."""

    new_grid_requested = pyqtSignal()
    load_grid_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {WHITE};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(0)

        layout.addStretch(2)

        # titre
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

        # boutons
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

        # signature
        lbl_credits = QLabel("Projet réalisé par Charly Deléglise, Selim Trilla et Younaïs Imamou")
        lbl_credits.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_credits.setStyleSheet("font-size: 9px; color: #444; font-weight: 500;")
        layout.addWidget(lbl_credits)


# == Page de jeu ====================================================================================================== #

class GamePage(QWidget):

    back_to_menu = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.grille = Grille(8, 8)
        self.grille.generate_motifs(min_size=2, max_size=5, hint_chance=0.25)

        self._build_ui()
        self.grille_widget.set_grille(self.grille)
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
        self.grille_widget = GrilleWidget()
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
        self.lbl_title = OutlinedLabel("NEONAURE")
        self.lbl_title.setFont(font_title)
        self.lbl_title.setFixedHeight(55)
        title_vbox.addWidget(self.lbl_title)

        fm = QFontMetrics(font_title)
        title_width = fm.horizontalAdvance("NEONAURE")

        double_line = QFrame()
        double_line.setFixedWidth(title_width)
        double_line.setFixedHeight(12)
        double_line.setStyleSheet(f"border-top: 3px solid {CYAN}; border-bottom: 3px solid {CYAN}; background-color: transparent;")
        title_vbox.addWidget(double_line)

        layout.addWidget(title_container)
        layout.addSpacerItem(QSpacerItem(0, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # case sélectionnée
        layout.addWidget(self._cell_info())

        # pavé numérique
        digit_container = QWidget()
        digit_layout = QHBoxLayout(digit_container)
        digit_layout.setContentsMargins(0, 0, 0, 0)
        digit_layout.addStretch()
        digit_layout.addWidget(self._digit_pad())
        digit_layout.addStretch()
        layout.addWidget(digit_container)
        layout.addSpacerItem(QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # barre supérieure
        line_above = QFrame()
        line_above.setFrameShape(QFrame.Shape.HLine)
        line_above.setStyleSheet(f"background-color: {CYAN}; max-height: 2px; min-height: 2px; border: none;")
        layout.addWidget(line_above)
        layout.addSpacerItem(QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # boutons d'action
        layout.addWidget(self._action_buttons())
        layout.addSpacerItem(QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # barre inférieure
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

        self.digit_buttons = []

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
            ("charger une grille", self._on_load, 0, 0),
            ("sauvegarder la grille", self._on_save, 0, 1),
            ("résoudre la grille", self._on_solve, 1, 0),
            ("avoir un indice", self._on_hint, 1, 1),
            ("nouvelle grille", self._on_new, 2, 0),
            ("menu principal", self._on_back_to_menu, 2, 1),
        ]

        for item in actions:
            label, slot, row, col = item[0], item[1], item[2], item[3]
            rowspan = item[4] if len(item) > 4 else 1
            colspan = item[5] if len(item) > 5 else 1

            btn = QPushButton(label)
            btn.setFixedHeight(36)
            btn.setStyleSheet(STYLE_ACTION_BTN)
            btn.clicked.connect(slot)
            grid.addWidget(btn, row, col, rowspan, colspan)

        return w

    def new_grid(self):
        """Génère une nouvelle grille aléatoire et l'affiche."""
        self.grille = Grille(8, 8)
        self.grille.generate_motifs(min_size=2, max_size=5, hint_chance=0.25)
        self.grille_widget.set_grille(self.grille)
        self.lbl_cell.setText("Aucune")

    def load_grid(self, file_path):
        """Charge une grille depuis un fichier JSON. Retourne True en cas de succès."""
        try:
            grille = Grille()
            grille.load_json(file_path)
            self.grille = grille
            self.grille_widget.set_grille(self.grille)
            self.lbl_cell.setText("Aucune")
            return True
        except Exception as e:
            QMessageBox.critical(self, "erreur", f"impossible de charger la grille :\n{e}")
            return False

    def _on_case_selected(self, case_ihm):
        self._update_cell_info()

    def _on_digit_clicked(self):
        sender = self.sender()
        for btn in self.digit_buttons:
            if btn is not sender:
                btn.setChecked(False)

        if sender.isChecked():
            value = int(sender.text())
            self.grille_widget.set_value(value)
            self._update_cell_info()
            self._check_victory()
        else:
            sender.setChecked(False)

    def _update_cell_info(self):
        case_ihm = self.grille_widget.get_selected_case()
        if case_ihm:
            case = case_ihm.case
            motif = self.grille.get_motif_of(case.get_x(), case.get_y())
            motif_name = motif.get_name() if motif else "?"
            motif_size = motif.get_size() if motif else "?"
            self.lbl_cell.setText(f"L{case.get_y()+1} C{case.get_x()+1}")
        else:
            self.lbl_cell.setText("aucune")

    def _check_victory(self):
        is_complete, _ = self.grille_widget.check_victory()
        if is_complete:
            QMessageBox.information(self, "bravo! !", "vous avez résolu la grille !!!! :)")

    def _on_load(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "charger une grille", "", "fichiers JSON (*.json);;tous les fichiers (*)")
        if file_path:
            if self.load_grid(file_path):
                QMessageBox.information(self, "chargement", f"grille chargée depuis {os.path.basename(file_path)}")

    def _on_save(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "sauvegarder la grille", "grille.json", "fichiers JSON (*.json);;tous les fichiers (*)")
        if file_path:
            try:
                self.grille.save_json(file_path)
                QMessageBox.information(self, "sauvegarde", f"grille sauvegardée dans {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "erreur", f"impossible de sauvegarder la grille :\n{e}")

    def _on_solve(self):
        reply = QMessageBox.question(self, "résoudre", "voulez vous avoir la solution de la grille ?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if Solver.solve(self.grille):
                self.grille_widget.refresh_all()
                QMessageBox.information(self, "résolution", "grille résolue !!")
            else:
                QMessageBox.warning(self, "résolution", "impossible de résoudre cette grille")

    def _on_hint(self):
        result = Solver.get_hint(self.grille)
        if result:
            x, y, value = result
            case = self.grille.get_case(x, y)
            case.set_value(value)
            self.grille_widget.refresh_all()
            QMessageBox.information(self, "indice", f"case L{y+1} C{x+1} = {value}")
        else:
            QMessageBox.warning(self, "indice", "aucun indice dispo :(")

    def _on_new(self):
        reply = QMessageBox.question(self, "nouvelle grille", "Voulez vous générer une nouvelle grille ? L'ancienne sera perdue si non sauvegardée",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.new_grid()
            QMessageBox.information(self, "nouvelle grille", "nouvelle grille générée !")

    def _on_back_to_menu(self):
        self.back_to_menu.emit()

    def keyPressEvent(self, event):
        text = event.text()
        if text.isdigit() and "1" <= text <= "5":
            value = int(text)
            self.grille_widget.set_value(value)
            self._update_cell_info()
            self._check_victory()
        elif event.key() in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete, Qt.Key.Key_0):
            self.grille_widget.set_value(0)
            self._update_cell_info()


# == Fenetre ============================================================================================================= #

class NeonaurWindow(QMainWindow):
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
        self.game_page = GamePage()

        self.stack.addWidget(self.start_page)
        self.stack.addWidget(self.game_page)
        self.stack.setCurrentWidget(self.start_page)

        self.start_page.new_grid_requested.connect(self._on_new_grid)
        self.start_page.load_grid_requested.connect(self._on_load_grid)
        self.game_page.back_to_menu.connect(self._on_back_to_menu)

    def _on_new_grid(self):
        self.game_page.new_grid()
        self.stack.setCurrentWidget(self.game_page)

    def _on_load_grid(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "charger une grille", "", "fichiers JSON (*.json);;tous les fichiers (*)")
        if file_path:
            if self.game_page.load_grid(file_path):
                QMessageBox.information(self, "chargement", f"grille chargée depuis {os.path.basename(file_path)}")
                self.stack.setCurrentWidget(self.game_page)

    def _on_back_to_menu(self):
        self.stack.setCurrentWidget(self.start_page)

    def keyPressEvent(self, event):
        if self.stack.currentWidget() is self.game_page:
            self.game_page.keyPressEvent(event)
        else:
            super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = NeonaurWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()