from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QTabWidget
from ui.mode_spec import ModeSpec
from ui.mode_rts import ModeRts
from ui.mode_zero_span import ModeZs

from fsw.device import RsFswInstrument


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Rhode&Schwarz FSW-43 GUI')
        my_icon = QIcon()
        my_icon.addFile('images\\crc_icon.ico')
        self.setWindowIcon(my_icon)
        
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        self.add_modes()
        
        self.instrument = RsFswInstrument.get_instance()
    
    
    def add_modes(self):
        mode_spec = ModeSpec()
        mode_rts = ModeRts()
        mode_zero_span = ModeZs()
        
        self.tab_widget.addTab(mode_spec, "Spectrum Mode")
        self.tab_widget.addTab(mode_rts, "Real-Time Spectrume Mode")
        self.tab_widget.addTab(mode_zero_span, "Zero Span Mode")
        
        # self.device = None
        
        # self.window_layout = QVBoxLayout()
        
        # self.title_layout = QHBoxLayout()
        # self.header_layout = QHBoxLayout()
        # self.content_layout = QHBoxLayout()
        
        # self.window_layout.addLayout(self.title_layout)
        # self.window_layout.addLayout(self.header_layout)
        # self.window_layout.addLayout(self.content_layout)
        
        # self.header = CommonHeader()
        
        # self.title = QLabel('Rhode&Schwarz FSW-43 GUI')
        
        # window_layout = QVBoxLayout()
        # window_layout.addWidget(self.header)
        
        # container = QWidget()
        # container.setLayout(window_layout)
        # self.setCentralWidget(container)
    
    
#     def spectrum_tab(self):
#         pass
    
    
#     def real_time_tab(self):
#         pass
    
    
#     def zero_span_tab(self):
#         pass

# class GUIWidgets(QWidget):
#     def __init__(self):
#         super().__init__()
    
    
#     def create_widgets(self):
        
#         self.widgets = {}
        
#         # Detectors
#         detectors = QComboBox()
#         detectors.addItem(['Auto Peak', 'Positive Peak', 'Negative Peak', 'RMS', 'Average', 'Sample'])
        
        
# class CommonHeader(QWidget):
#     def __init__(self):
#         super().__init__()
        
#         self.create_widgets()
        
#         self.set_layout()
    
    
#     def create_widgets(self):
        
#         self.ip_entry_label = QLabel('Enter IP Address:')
        
#         self.ip_entry = QLineEdit()
#         self.ip_entry.setInputMask('000.000.000.000;_')
#         self.ip_entry.setFixedWidth(85)
#         self.ip_entry.returnPressed.connect(self.connect_device)
        
#         self.connect_button = QPushButton('Connect')
#         self.connect_button.pressed.connect(self.connect_device)
        
#         self.visa_tout_label = QLabel('VISA Timeout (ms):')
        
#         self.visa_tout_entry = QLineEdit()
#         self.visa_tout_entry.setPlaceholderText('3000')
        
#         self.opc_tout_label = QLabel('OPC Timeout (ms):')
        
#         self.opc_tout_entry = QLineEdit()
#         self.opc_tout_entry.setPlaceholderText('3000')
        
#         # self.load_button = QPushButton('Load Config')
#         # self.load_button.setFixedWidth(100)
        
#         # self.save_button = QPushButton('Save Config')
#         # self.save_button.setFixedWidth(100)
        
#         # img= QImage('crc_icon.png')
#         # pixmap = QPixmap(img.scaledToWidth(120))
#         # self.crc_logo = QLabel(self)
#         # self.crc_logo.setPixmap(pixmap)
    
    
#     def set_layout(self):
#         ip_entry_layout1 = QVBoxLayout()
#         ip_entry_layout2 = QHBoxLayout()
#         ip_entry_layout2.addWidget(self.ip_entry)
#         ip_entry_layout2.addWidget(self.connect_button)
#         ip_entry_layout1.addWidget(self.ip_entry_label)
#         ip_entry_layout1.addLayout(ip_entry_layout2)
        
#         visa_layout = QVBoxLayout()
#         visa_layout.addWidget(self.visa_tout_label)
#         visa_layout.addWidget(self.visa_tout_entry)
        
#         opc_layout = QVBoxLayout()
#         opc_layout.addWidget(self.opc_tout_label)
#         opc_layout.addWidget(self.opc_tout_entry)
        
#         # save_layout = QVBoxLayout()
#         # save_layout.addWidget(self.load_button)
#         # save_layout.addWidget(self.save_button)
        
#         header_layout = QHBoxLayout()
#         header_layout.addLayout(ip_entry_layout1)
#         header_layout.addLayout(visa_layout)
#         header_layout.addLayout(opc_layout)
#         #header_layout.addLayout(save_layout)
#         #header_layout.addWidget(self.crc_logo)
        
#         self.setLayout(header_layout)
        
#         self.set_stylesheet()
    
    
#     def connect_device(self):
#         print('I would try to connect to FSW now!')
