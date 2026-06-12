import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QGridLayout, QLabel, 
                             QStatusBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

import os
base_dir = os.path.dirname(os.path.abspath(__file__))
modele_dir = os.path.join(base_dir, "modele")
if modele_dir not in sys.path:
    sys.path.insert(0, modele_dir)


class caseihm(QPushButton):
    def __init__(self, ligne, colonne, parent=None):
        super().__init__(parent)
        self.ligne = ligne
        self.colonne = colonne
        self.valeur = 0
        self.id_motif = None
        
        self.setFixedSize(55, 55)
        self.setFont(QFont("segoe ui", 16, QFont.Weight.Bold))
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def configurer_motif(self, id_motif, bordures_grasses=None):
        self.id_motif = id_motif
        
        b_top = "3px solid #2c3e50" if bordures_grasses and "top" in bordures_grasses else "1px solid #bdc3c7"
        b_bottom = "3px solid #2c3e50" if bordures_grasses and "bottom" in bordures_grasses else "1px solid #bdc3c7"
        b_left = "3px solid #2c3e50" if bordures_grasses and "left" in bordures_grasses else "1px solid #bdc3c7"
        b_right = "3px solid #2c3e50" if bordures_grasses and "right" in bordures_grasses else "1px solid #bdc3c7"

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #ffffff;
                border-top: {b_top};
                border-bottom: {b_bottom};
                border-left: {b_left};
                border-right: {b_right};
                color: #2c3e50;
                border-radius: 0px;
            }}
            QPushButton:hover {{
                background-color: #eaeded;
            }}
            QPushButton:focus {{
                background-color: #ebf5fb;
                border: 2px solid #3498db;
            }}
        """)

    def fixer_valeur(self, num):
        self.valeur = num
        self.setText(str(num) if num > 0 else "")


class neonauresimplifie(QMainWindow):
    def __init__(self):
        super().__init__()
        self.case_selectionnee = None
        self.setWindowTitle("neonaure - ihm")
        self.resize(500, 500)
        
        self.init_ui()
        # creation de la grille par defaut : 6 motifs de 2x3 (6 lignes, 6 colonnes)
        self.creer_grille_defaut()

    def init_ui(self):
        centre_widget = QWidget()
        layout_principal = QVBoxLayout(centre_widget)
        
        self.layout_grille = QGridLayout()
        self.layout_grille.setSpacing(0)
        
        layout_grille_centre = QHBoxLayout()
        layout_grille_centre.addStretch()
        layout_grille_centre.addLayout(self.layout_grille)
        layout_grille_centre.addStretch()
        layout_principal.addLayout(layout_grille_centre)
        
        label_clavier = QLabel("choisissez une case, puis un chiffre :")
        label_clavier.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(label_clavier)
        
        layout_chiffres = QHBoxLayout()
        
        btn_gomme = QPushButton("⌫")
        btn_gomme.setFixedSize(40, 40)
        btn_gomme.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
        btn_gomme.clicked.connect(lambda: self.clavier_chiffre_clique(0))
        layout_chiffres.addWidget(btn_gomme)
        
        for i in range(1, 7):
            btn = QPushButton(str(i))
            btn.setFixedSize(40, 40)
            btn.setFont(QFont("arial", 12, QFont.Weight.Bold))
            btn.setStyleSheet("background-color: #34495e; color: white;")
            btn.clicked.connect(lambda checked, val=i: self.clavier_chiffre_clique(val))
            layout_chiffres.addWidget(btn)
            
        layout_principal.addLayout(layout_chiffres)
        
        self.barre_statut = QStatusBar()
        self.setStatusBar(self.barre_statut)
        self.barre_statut.showMessage("pret, cliquez sur une case")
        
        self.setCentralWidget(centre_widget)

    def creer_grille_defaut(self):
        # genere une grille de 6x6 decoupee en 6 blocs de 2 lignes x 3 colonnes
        self.cases = {}
        lignes = 6
        colonnes = 6
        
        for r in range(lignes):
            for c in range(colonnes):
                case = caseihm(r, c)
                case.clicked.connect(lambda checked, item=case: self.case_cliquee(item))
                
                # calcul de l'id du motif (0 a 5) pour des blocs de 2x3
                id_motif = (r // 2) * 2 + (c // 3)
                
                # definition des contours epais pour les blocs de 2x3
                b_grasses = []
                if r % 2 == 0: b_grasses.append("top")
                if r % 2 == 1: b_grasses.append("bottom")
                if c % 3 == 0: b_grasses.append("left")
                if c % 3 == 2: b_grasses.append("right")
                
                case.configurer_motif(id_motif, b_grasses)
                self.layout_grille.addWidget(case, r, c)
                self.cases[(r, c)] = case

    def case_cliquee(self, case):
        self.case_selectionnee = case
        self.barre_statut.showMessage(f"case : L{case.ligne + 1} C{case.colonne + 1} | motif {case.id_motif}")

    def clavier_chiffre_clique(self, valeur):
        if self.case_selectionnee:
            self.case_selectionnee.fixer_valeur(valeur)
            self.barre_statut.showMessage(f"valeur {valeur} placee en L{self.case_selectionnee.ligne + 1} C{self.case_selectionnee.colonne + 1}")
        else:
            self.barre_statut.showMessage("erreur")

    def keyPressEvent(self, event):
        if self.case_selectionnee:
            texte = event.text()
            if texte.isdigit() and "1" <= texte <= "6":
                self.clavier_chiffre_clique(int(texte))
            elif event.key() in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete, Qt.Key.Key_0):
                self.clavier_chiffre_clique(0)

def test_backend_imports():
    print("--- Test des imports du backend ---")
    
    modules = {
        "Case": "modele.Case",
        "Motif": "modele.Motif",
        "Solver": "modele.Solver",
        "Validator": "modele.Validator",
        "LevelGenerator": "modele.LevelGenerator"
    }

    for nom, chemin in modules.items():
        try:
            mod = __import__(chemin, fromlist=[nom])
            cls = getattr(mod, nom)
            print(f"✅ {nom} importé avec succès depuis {chemin}")
        except Exception as e:
            print(f"❌ Erreur lors de l'import de {nom} : {e}")

    print("-----------------------------------")

if __name__ == "__main__":
    test_backend_imports()
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    fenetre = neonauresimplifie()
    fenetre.show()
    sys.exit(app.exec())