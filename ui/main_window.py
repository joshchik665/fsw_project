from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
)
from ui.mode_spec import ModeSpec
from ui.mode_rts import ModeRts
from ui.mode_zero_span import ModeZs
from fsw.settings_manager import SettingsManager


class MainWindow(QMainWindow):
    def __init__(self, config, visa_timeout, opc_timeout):
        super().__init__()
        
        self.instrument = SettingsManager(config['ip_address'],r"configs\default\default.json", visa_timeout, opc_timeout)
        
        self._set_title_and_window()
        self._create_tabs()
        
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Connected to Rhode&Schwarz FSW-43 @' + config['ip_address'], timeout=0)
        
        if config['data']:
            self.tab_widget.setCurrentIndex(self.tab_index[config['mode']])
    
    
    def _set_title_and_window(self):
        self.setWindowTitle('Rhode&Schwarz FSW-43 GUI')
        my_icon = QIcon()
        my_icon.addFile('images\\crc_icon.ico')
        self.setWindowIcon(my_icon)
    
    
    def _create_tabs(self):
        self.tab_widget = QTabWidget()
        
        self.setCentralWidget(self.tab_widget)
        
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        self.current_tab_index = 0
        
        self.tab_index = {
            "Spectrum": 0,
            "Real-Time Spectrum": 1,
            "Zero-Span": 2,
        }
        
        mode_spec = ModeSpec(self.instrument,self.tab_widget)
        mode_rts = ModeRts(self.instrument,self.tab_widget)
        mode_zero_span = ModeZs(self.instrument,self.tab_widget)
        
        self.tab_widget.addTab(mode_spec, "Spectrum Mode")
        self.tab_widget.addTab(mode_rts, "Real-Time Spectrume Mode")
        self.tab_widget.addTab(mode_zero_span, "Zero Span Mode")
    
    
    def on_tab_changed(self, new_tab_index):
        current_tab_widget = self.tab_widget.widget(new_tab_index)

        current_tab_widget.set_mode()
        current_tab_widget.verify()
        
        self.current_tab_index = new_tab_index