# connect_dialog.py

from PySide6.QtWidgets import (
    QDialog, 
    QVBoxLayout, 
    QLabel, 
    QLineEdit, 
    QPushButton,
    QHBoxLayout,
) 
from PySide6.QtGui import QIcon
import json
from ui.common.utilities import open_file_dialog


class IpEntryDialog(QDialog):
    def __init__(self):
        """Custom Dialog that appears to the user when the first start the program. Gets the IP address of the instrument or a config file"""
        super().__init__()
        
        self._set_title_and_window()
        self._set_widgets()
    
    
    def _set_title_and_window(self) -> None:
        """Set the title of the widget an icon"""
        self.setWindowTitle('Signal Analyzer GUI')
        my_icon = QIcon()
        my_icon.addFile('images\\crc_icon.ico')
        self.setWindowIcon(my_icon)
    
    
    def _set_widgets(self) -> None:
        """Creates the widgets on this window"""
        # Layouts
        self.layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        self.setLayout(self.layout)
        
        # head line
        self.label = QLabel("Enter the IP address of the instrument:")
        self.layout.addWidget(self.label)
        
        # line to enter the IP address
        self.ip_input = QLineEdit()
        self.ip_input.returnPressed.connect(self.on_confirm)
        self.layout.addWidget(self.ip_input)
        
        # add the button on the bottom of the window
        self.confirm_button = QPushButton("Connect")
        self.confirm_button.clicked.connect(self.on_confirm)
        layout1.addWidget(self.confirm_button)
        
        self.load_button = QPushButton('Load Config')
        self.load_button.clicked.connect(self.load_settings)
        layout1.addWidget(self.load_button)
        
        self.layout.addLayout(layout1)
    
    
    def load_settings(self) -> None:
        """Prompts the user to select a file to load from, stores the config of the file, and closes the window"""
        filepath = open_file_dialog('Open JSON file', r'user_configs', '.json', self)
        
        if filepath:
            with open(filepath, 'r') as file:
                self.config = json.load(file)
            
            self.accept()
    
    
    def on_confirm(self) -> None:
        """Closes this window and saves the ip address"""
        ip_address = self.ip_input.text()
        
        self.config = {
            'ip_address': ip_address, 
            'data': {}
        }
        
        self.accept()








