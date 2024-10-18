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
        
        self.instrument = SettingsManager("192.168.2.226",r"configs\default\default.json")
        
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
        
        self.set_status_label = QLabel("-> ")
        set_setting_layout.addWidget(self.set_status_label)
        
        layout.addLayout(set_setting_layout)
        
        verify_setting_layout = QHBoxLayout()
        
        verify_setting_label = QLabel("Verify Setting: ")
        verify_setting_layout.addWidget(verify_setting_label)
        
        self.verify_setting_entry = QLineEdit()
        verify_setting_layout.addWidget(self.verify_setting_entry)
        
        self.verify_setting_button = QPushButton("Verify")
        self.verify_setting_button.pressed.connect(self.verify_setting)
        verify_setting_layout.addWidget(self.verify_setting_button)
        
        self.verify_status_label = QLabel("-> ")
        verify_setting_layout.addWidget(self.verify_status_label)
        
        layout.addLayout(verify_setting_layout)
        
        set_mode_layout = QHBoxLayout()
        
        set_mode_label = QLabel("Set Mode: ")
        set_mode_layout.addWidget(set_mode_label)
        
        self.set_mode_entry = QLineEdit()
        set_mode_layout.addWidget(self.set_mode_entry)
        
        self.set_mode_button = QPushButton("Set Mode")
        self.set_mode_button.pressed.connect(self.set_mode)
        set_mode_layout.addWidget(self.set_mode_button)
        
        layout.addLayout(set_mode_layout)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    
    def apply_setting(self):
        response = self.instrument.set_setting(self.setting_name.text(), self.setting_value.text())
        self.set_status_label.setText(f"-> {response}")
    
    
    def verify_setting(self):
        response = self.instrument.verify_setting(self.verify_setting_entry.text())
        self.verify_status_label.setText(f"-> {response}")
    
    
    def set_mode(self):
        self.instrument.set_mode(self.set_mode_entry.text())


app = QApplication(sys.argv)
stylesheet = load_stylesheet("styles/style.qss")
app.setStyleSheet(stylesheet)
window = MainWindow()
window.show()
app.exec()

