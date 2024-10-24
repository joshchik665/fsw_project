from PySide6.QtWidgets import (
    QDialog, 
    QVBoxLayout, 
    QLabel, 
    QLineEdit, 
    QPushButton,
    QHBoxLayout,
) 
from PySide6.QtGui import QIcon, QDoubleValidator
import json
import common.utilities as util


class IpEntryDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self._set_title_and_window()
        self._set_widgets()
    
    
    def _set_title_and_window(self) -> None:
        self.setWindowTitle('Rhode&Schwarz FSW-43 GUI')
        my_icon = QIcon()
        my_icon.addFile('images\\crc_icon.ico')
        self.setWindowIcon(my_icon)
    
    
    def _set_widgets(self) -> None:
        self.layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        self.setLayout(self.layout)
        
        self.label = QLabel("Enter the IP address of the instrument:")
        self.layout.addWidget(self.label)
        
        self.ip_input = QLineEdit()
        self.ip_input.returnPressed.connect(self.on_confirm)
        self.layout.addWidget(self.ip_input)
        
        visa_label = QLabel('Set Visa Timeout(ms):')
        self.layout.addWidget(visa_label)
        
        self.visa_entry = QLineEdit()
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        # Set the range (optional, adjust as needed)
        #validator.setRange(-999999.99, 999999.99, 2)  # 2 decimal places
        self.visa_entry.setValidator(validator)
        self.visa_entry.setPlaceholderText('3000')
        self.visa_entry.setFixedSize(100, 25)
        self.layout.addWidget(self.visa_entry)
        
        opc_label = QLabel('Set Opc Timeout(ms):')
        self.layout.addWidget(opc_label)
        
        self.opc_entry = QLineEdit()
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        # Set the range (optional, adjust as needed)
        #validator.setRange(-999999.99, 999999.99, 2)  # 2 decimal places
        self.opc_entry.setValidator(validator)
        self.opc_entry.setPlaceholderText('3000')
        self.opc_entry.setFixedSize(100, 25)
        self.layout.addWidget(self.opc_entry)
        
        self.confirm_button = QPushButton("Connect")
        self.confirm_button.clicked.connect(self.on_confirm)
        layout1.addWidget(self.confirm_button)
        
        self.load_button = QPushButton('Load Config')
        self.load_button.clicked.connect(self.load_settings)
        layout1.addWidget(self.load_button)
        
        self.layout.addLayout(layout1)
    
    
    def get_timeouts(self) -> None:
        self.visa_timeout = self.visa_entry.text()
        self.opc_timeout = self.opc_entry.text()
        
        if not self.visa_timeout:
            self.visa_timeout = 3000
        
        if not self.opc_timeout:
            self.opc_timeout = 3000
        
        self.visa_timeout = int(self.visa_timeout)
        self.opc_timeout = int(self.opc_timeout)
    
    
    def load_settings(self) -> None:
        filepath = util.open_file_dialog('Open JSON file', '.json', self)
        
        self.get_timeouts()
        
        if filepath:
            with open(filepath, 'r') as file:
                self.config = json.load(file)
            
            self.accept()
    
    
    def on_confirm(self) -> None:
        ip_address = self.ip_input.text()
        
        self.get_timeouts()
        
        self.config = {
            'ip_address': ip_address, 
            'data': {}
        }
        
        self.accept()