from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
)
from PySide6.QtCore import Signal
from ui.mode_spec import ModeSpec
from ui.mode_rts import ModeRts
from ui.mode_zero_span import ModeZs
from fsw.settings_manager import SettingsManager


class MainWindow(QMainWindow):
    def __init__(self, config, visa_timeout, opc_timeout):
        super().__init__()
        
        self.tab_indicies = {
            "Spectrum": 0,
            "Real-Time Spectrum": 1,
            "Zero-Span": 2,
        }
        self._programmatic_change = False
        
        self._set_title_and_window()
        
        self.instrument = SettingsManager(
            config['ip_address'],
            r"configs\default\default.json", 
            visa_timeout, 
            opc_timeout
            )
        
        self._set_status_bar(config['ip_address'])
        
        self._create_tabs()
        
        current_tab_widget = self.tab_widget.widget(self.current_tab_index)
        if config['data']:
            current_tab_widget.load_settings(config)
        else:
            current_tab_widget.verify()
            
            
    
    
    def _set_title_and_window(self):
        self.setWindowTitle('Rhode&Schwarz FSW-43 GUI')
        my_icon = QIcon()
        my_icon.addFile('images\\crc_icon.ico')
        self.setWindowIcon(my_icon)
    
    
    def _set_status_bar(self, ip_address):
        status_bar = self.statusBar()
        status_bar.showMessage(
            f'Connected to Rhode&Schwarz FSW-43 @ {ip_address}', 
            timeout=0
            )
    
    
    def _create_tabs(self):
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        self.current_tab_index = 0
        
        self.tab_widget.addTab(ModeSpec(self.instrument, self.tab_widget), "Spectrum Mode")
        self.tab_widget.addTab(ModeRts(self.instrument, self.tab_widget), "Real-Time Spectrume Mode")
        self.tab_widget.addTab(ModeZs(self.instrument, self.tab_widget), "Zero Span Mode")
        
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
    
    
    def on_tab_changed(self, new_tab_index):
        new_tab_widget = self.tab_widget.widget(new_tab_index)
        
        new_tab_widget.set_mode()
        
        if not self._programmatic_change:
            new_tab_widget.verify()
        
        self.current_tab_index = new_tab_index
    
    
    def change_tab_programmatically(self, index):
        self._programmatic_change = True
        self.tab_widget.setCurrentIndex(index)
        self._programmatic_change = False
