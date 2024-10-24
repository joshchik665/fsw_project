# connect_dialog.py

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
from ui.common.utilities import open_file_dialog


class IpEntryDialog(QDialog):
    def __init__(self):
        """Custom Dialog that appears to the user when the first start the program. Gets the IP address of the instrument or a config file
        """
        super().__init__()
        
        self._set_title_and_window()
        self._set_widgets()
    
    
    def _set_title_and_window(self) -> None:
        """Set the title of the widget an icon
        """
        self.setWindowTitle('Rhode&Schwarz FSW-43 GUI')
        my_icon = QIcon()
        my_icon.addFile('images\\crc_icon.ico')
        self.setWindowIcon(my_icon)
    
    
    def _set_widgets(self) -> None:
        """Creates the widgets on this window
        """
        # Layouts
        self.layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        self.setLayout(self.layout)
        
        # head line
        self.label = QLabel("Enter the IP address of the instrument:")
        self.layout.addWidget(self.label)
        
        # line to enter the IP address
        self.ip_input = QLineEdit()
        self.ip_input.returnPressed.connect(self.on_confirm)
        self.layout.addWidget(self.ip_input)
        
        # Create the entry boxes for the visa timeout
        visa_label = QLabel('Set Visa Timeout(ms):')
        layout1.addWidget(visa_label)
        
        self.visa_entry = QLineEdit()
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.visa_entry.setValidator(validator)
        self.visa_entry.setPlaceholderText('3000')
        self.visa_entry.setFixedSize(100, 25)
        layout1.addWidget(self.visa_entry)
        
        self.layout.addLayout(layout1)
        
        # Create the entry boxes for the opc timeout
        opc_label = QLabel('Set Opc Timeout(ms):')
        layout2.addWidget(opc_label)
        
        self.opc_entry = QLineEdit()
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.opc_entry.setValidator(validator)
        self.opc_entry.setPlaceholderText('3000')
        self.opc_entry.setFixedSize(100, 25)
        layout2.addWidget(self.opc_entry)
        
        self.layout.addLayout(layout2)
        
        # add the button on the bottom of the window
        self.confirm_button = QPushButton("Connect")
        self.confirm_button.clicked.connect(self.on_confirm)
        layout3.addWidget(self.confirm_button)
        
        self.load_button = QPushButton('Load Config')
        self.load_button.clicked.connect(self.load_settings)
        layout3.addWidget(self.load_button)
        
        self.layout.addLayout(layout3)
    
    
    def get_timeouts(self) -> None:
        """Gets the value in the timeout entry and saves them
        """
        # Get current text
        self.visa_timeout = self.visa_entry.text()
        self.opc_timeout = self.opc_entry.text()
        
        # if nothing is there, use defaults
        if not self.visa_timeout:
            self.visa_timeout = 3000
        if not self.opc_timeout:
            self.opc_timeout = 3000
        
        # save them as int
        self.visa_timeout = int(self.visa_timeout)
        self.opc_timeout = int(self.opc_timeout)
    
    
    def load_settings(self) -> None:
        """Prompts the user to select a file to load from, stores the config of the file, and closes the window
        """
        filepath = open_file_dialog('Open JSON file', '.json', self)
        
        self.get_timeouts()
        
        if filepath:
            with open(filepath, 'r') as file:
                self.config = json.load(file)
            
            self.accept()
    
    
    def on_confirm(self) -> None:
        """Closes this window and saves the ip address
        """
        ip_address = self.ip_input.text()
        
        self.get_timeouts()
        
        self.config = {
            'ip_address': ip_address, 
            'data': {}
        }
        
        self.accept()