import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout,
    QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt, QSize, QTimer


class Cell(QPushButton):
    """Une simple case visuelle, sans logique."""
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(40, 40))
        self.setStyleSheet("""
            QPushButton {
                background-color: #d7dce1;
                border: 1px solid #9aa5b1;
            }
            QPushButton:hover {
                background-color: #c5ccd3;
            }
        """)


class MineSweeperUI(QWidget):
    """Interface minimaliste : barre supérieure + grille."""
    def __init__(self, rows=10, cols=10, bombs=10):
        super().__init__()

        self.rows = rows
        self.cols = cols
        self.bombs = bombs
        self.time_elapsed = 0
        self.is_paused = False

        self.setWindowTitle("Démineur")
        self.setFixedSize(420, 450)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)
        self.setLayout(main_layout)

  
        # -------------------------------------------------
        #  GRILLE
        # -------------------------------------------------
        grid = QGridLayout()
        grid.setSpacing(0)

        for r in range(self.rows):
            for c in range(self.cols):
                grid.addWidget(Cell(), r, c)

        main_layout.addLayout(grid)


# ---------------------------------------------------------
#  Lancement
# ---------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MineSweeperUI()
    window.show()
    sys.exit(app.exec())
