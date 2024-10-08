from PySide6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
)
from PySide6.QtGui import (
    QIcon,
    QPixmap,
    QImage,
)
from PySide6.QtCore import (
    Qt,
    Slot,
)
from fsw.device import RsFswInstrument

class ModeSuper(QWidget):
    def __init__(self):
        super().__init__()
        
        self.window_layout = QVBoxLayout()
        
        self.title_layout = QHBoxLayout()
        self.header_layout = QHBoxLayout()
        self.content_layout = QHBoxLayout()
        
        self.window_layout.addLayout(self.title_layout)
        self.window_layout.addLayout(self.header_layout)
        self.window_layout.addStretch(1)
        self.window_layout.addLayout(self.content_layout)
        
        self.instrument = RsFswInstrument.get_instance()
        
        self.mode_index = {
            '0': 'Spectrum',
            '1': 'Real-Time Spectrum',
            '2': 'Zero-Span'
        }
        
        self.mode_scpi_commands = {
            'Spectrum': "SANALYZER",
            'Real-Time Spectrum': "RTIM",
            'Zero-Span': 'SANALYZER',
        }
        
        self.mode = ''
        
        self._set_title()
        
        self._set_header()
    
    
    def _set_title(self):
        title = QLabel('Rhode & Schwarz FSW-43 GUI')
        title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        title.setObjectName('title')
        
        img= QImage('images\\crc_icon.png')
        pixmap = QPixmap(img.scaledToWidth(100))
        crc_logo = QLabel(self)
        crc_logo.setPixmap(pixmap)
        crc_logo.setAlignment(Qt.AlignRight | Qt.AlignTop)
        
        layout = QHBoxLayout()
        layout.addWidget(title)
        layout.addWidget(crc_logo)
        
        self.title_layout.addLayout(layout)
    
    
    def _set_header(self):
        self.load_button = QPushButton('Load Config')
        
        self.save_button = QPushButton('Save Config')
        
        visa_label = QLabel('Visa Timeout(ms):')
        
        self.visa_entry = QLineEdit()
        self.visa_entry.setPlaceholderText('3000')
        self.visa_entry.setFixedWidth(100)
        
        opc_label = QLabel('Opc Timeout(ms):')
        
        self.opc_entry = QLineEdit()
        self.opc_entry.setPlaceholderText('3000')
        self.opc_entry.setFixedWidth(100)
        
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        
        layout = QHBoxLayout()
        layout.addLayout(layout1)
        layout.addStretch(1)
        layout.addLayout(layout2)
        
        layout1.setAlignment(Qt.AlignLeft)
        layout2.setAlignment(Qt.AlignRight)
        
        layout1.addWidget(self.load_button)
        layout1.addWidget(self.save_button)
        
        layout2.addWidget(visa_label)
        layout2.addWidget(self.visa_entry)
        layout2.addWidget(opc_label)
        layout2.addWidget(self.opc_entry)
        
        self.header_layout.addLayout(layout)
    
    
    def configure(self):
        self.instrument.configure()
    
    
    def activate(self,previous_index):
        self.instrument.write_str_with_opc(f"INST:CRE:REPL '{self.mode_index[str(previous_index)]}', {self.mode_scpi_commands[self.mode]}, '{self.mode}'")
        


