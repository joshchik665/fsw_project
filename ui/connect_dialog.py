from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from fsw.device import RsFswInstrument

class IpEntryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Device IP")
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.label = QLabel("Enter the IP address of the instrument:")
        self.layout.addWidget(self.label)
        
        self.ip_input = QLineEdit()
        self.layout.addWidget(self.ip_input)
        
        self.confirm_button = QPushButton("Connect")
        self.confirm_button.clicked.connect(self.on_confirm)
        self.layout.addWidget(self.confirm_button)
        
    def on_confirm(self):
        ip_address = self.ip_input.text()
        self.instrument = RsFswInstrument(ip_address)
        self.accept()