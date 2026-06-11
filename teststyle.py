import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

CYAN       = "#00CCCC"
GREY       = "#C8C8C8"
WHITE      = "#FFFFFF"

class CaseIHM(QLabel):
    clicked = pyqtSignal(object)

    def __init__(self, ligne, colonne, parent=None):
        super().__init__(parent)
        self.ligne = ligne
        self.colonne = colonne
        self.valeur = 0
        self.bordures = []
        
        self.setFixedSize(60, 60)
        self.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def configurer_bordures(self, bordures_grasses):
        self.bordures = bordures_grasses
        self.mettre_a_jour_style(False)

    def mettre_a_jour_style(self, selectionnee=False):
        b_top    = f"3px solid {CYAN}" if "top" in self.bordures else f"1px solid {GREY}"
        b_bottom = f"3px solid {CYAN}" if "bottom" in self.bordures else f"1px solid {GREY}"
        b_left   = f"3px solid {CYAN}" if "left" in self.bordures else f"1px solid {GREY}"
        b_right  = f"3px solid {CYAN}" if "right" in self.bordures else f"1px solid {GREY}"
        
        bg_color = "#DAEEF0" if selectionnee else WHITE
        
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                border-top: {b_top};
                border-bottom: {b_bottom};
                border-left: {b_left};
                border-right: {b_right};
                color: #2c3e50;
            }}
        """)

    def fixer_valeur(self, num):
        self.valeur = num
        self.setText(str(num) if num > 0 else "")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self)


class NeonaurGrilleSeule(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("test mais stylé")
        self.setStyleSheet(f"QMainWindow {{ background-color: {WHITE}; }}")
        
        self.case_selectionnee = None
        self.init_ui()

    def init_ui(self):
        centre_widget = QWidget()
        self.setCentralWidget(centre_widget)
        
        main_layout = QVBoxLayout(centre_widget)
        center_layout = QHBoxLayout()
        
        self.layout_grille = QGridLayout()
        self.layout_grille.setSpacing(0) 
        
        center_layout.addStretch()
        center_layout.addLayout(self.layout_grille)
        center_layout.addStretch()
        
        main_layout.addStretch()
        main_layout.addLayout(center_layout)
        main_layout.addStretch()
        
        self.creer_grille_6x6()

    def creer_grille_6x6(self):
        self.cases = {}
        for r in range(6):
            for c in range(6):
                case = CaseIHM(r, c)
                case.clicked.connect(self.case_cliquee)
                
                b_grasses = []
                if r % 2 == 0: b_grasses.append("top")
                if r % 2 == 1: b_grasses.append("bottom")
                if c % 3 == 0: b_grasses.append("left")
                if c % 3 == 2: b_grasses.append("right")
                
                case.configurer_bordures(b_grasses)
                self.layout_grille.addWidget(case, r, c)
                self.cases[(r, c)] = case

    def case_cliquee(self, case):
        if self.case_selectionnee:
            self.case_selectionnee.mettre_a_jour_style(selectionnee=False)
        
        self.case_selectionnee = case
        self.case_selectionnee.mettre_a_jour_style(selectionnee=True)

    def keyPressEvent(self, event):
        if self.case_selectionnee:
            texte = event.text()
            # Seuls les chiffres de 1 à 5 sont acceptés (6 à 9 sont bloqués ici)
            if texte.isdigit() and "1" <= texte <= "5":
                self.case_selectionnee.fixer_valeur(int(texte))
            # Permet toujours d'effacer avec Retour Arrière, Suppr ou 0
            elif event.key() in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete, Qt.Key.Key_0):
                self.case_selectionnee.fixer_valeur(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    fenetre = NeonaurGrilleSeule()
    fenetre.resize(450, 450)
    fenetre.show()
    sys.exit(app.exec())