import sys
from PyQt6.QtWidgets import QApplication
from controllers.main_controller import MainController


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainController()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()