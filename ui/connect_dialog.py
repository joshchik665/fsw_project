from PySide6.QtWidgets import (
    QDialog, 
    QVBoxLayout, 
    QLabel, 
    QLineEdit, 
    QPushButton,
    QHBoxLayout,
) 

import json
import common.utilities as util

class IpEntryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Device IP")
        
        self.layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        self.setLayout(self.layout)
        
        self.label = QLabel("Enter the IP address of the instrument:")
        self.layout.addWidget(self.label)
        
        self.ip_input = QLineEdit()
        self.ip_input.returnPressed.connect(self.on_confirm)
        self.layout.addWidget(self.ip_input)
        
        self.confirm_button = QPushButton("Connect")
        self.confirm_button.clicked.connect(self.on_confirm)
        layout1.addWidget(self.confirm_button)
        
        self.load_button = QPushButton('Load Config')
        self.load_button.clicked.connect(self.load_settings)
        layout1.addWidget(self.load_button)
        
        self.layout.addLayout(layout1)
    
    
    def load_settings(self):
        filepath = util.open_file_dialog('Open JSON file', '.json', self)
        
        if filepath:
            with open(filepath, 'r') as file:
                self.config = json.load(file)
            
            self.accept()
    
    
    def on_confirm(self):
        ip_address = self.ip_input.text()
        
        self.config = {
            'ip_address': ip_address, 
            'data': {}
        }
        
        self.accept()