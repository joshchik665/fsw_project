from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
    QTabWidget,
    QStatusBar,
    QFileDialog,
)
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('FSW43 GUI')
        my_icon = QIcon()
        my_icon.addFile('crc_icon.ico')
        self.setWindowIcon(my_icon)
    
    
    def create_widgets(self):
        pass


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()