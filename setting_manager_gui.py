from fsw.settings_manager import SettingsManager
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel
from PySide6.QtGui import QIcon
import sys


def load_stylesheet(filename):
    with open(filename, "r") as file:
        return file.read()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.instrument = SettingsManager("192.168.2.226")
        
        self.setWindowTitle('Rhode&Schwarz FSW-43 GUI')
        my_icon = QIcon()
        my_icon.addFile('images\\crc_icon.ico')
        self.setWindowIcon(my_icon)
        
        layout = QVBoxLayout()
        
        title = QLabel("SettingsManager testing GUI")
        layout.addWidget(title)
        
        set_setting_layout = QHBoxLayout()
        
        set_setting_label = QLabel("Set Setting: ")
        set_setting_layout.addWidget(set_setting_label)
        
        self.setting_name = QLineEdit()
        set_setting_layout.addWidget(self.setting_name)
        
        self.setting_value = QLineEdit()
        set_setting_layout.addWidget(self.setting_value)
        
        self.apply_button = QPushButton("Apply")
        self.apply_button.pressed.connect(self.apply_setting)
        set_setting_layout.addWidget(self.apply_button)
        
        self.status_label = QLabel("-> ")
        set_setting_layout.addWidget(self.status_label)
        
        layout.addLayout(set_setting_layout)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    
    def apply_setting(self):
        response = self.instrument.set_setting(self.setting_name.text(), self.setting_value.text())
        self.status_label.setText(f"-> {response}")


app = QApplication(sys.argv)
stylesheet = load_stylesheet("styles/style.qss")
app.setStyleSheet(stylesheet)
window = MainWindow()
window.show()
app.exec()

