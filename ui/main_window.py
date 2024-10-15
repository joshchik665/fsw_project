from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
)

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
        
        self._previous_index = 0
        
        self.status_bar = self.statusBar()
        
        self.add_modes()
        
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        instrument = RsFswInstrument.get_instance()
        
        self.status_bar.showMessage('Connected to Rhode&Schwarz FSW-43 @' + instrument.ip_address, timeout=0)
        
        self.tab_widget.setCurrentIndex(self.tab_index[instrument.mode])
        
        
    
    
    def add_modes(self):
        self.tab_index = {
            "Spectrum": 0,
            "Real-Time Spectrum": 1,
            "Zero-Span": 2,
        }
        
        mode_spec = ModeSpec()
        mode_rts = ModeRts()
        mode_zero_span = ModeZs()
        
        self.tab_widget.addTab(mode_spec, "Spectrum Mode")
        self.tab_widget.addTab(mode_rts, "Real-Time Spectrume Mode")
        self.tab_widget.addTab(mode_zero_span, "Zero Span Mode")
    
    
    def on_tab_changed(self, index):
        current_widget = self.tab_widget.widget(index)
        if current_widget and hasattr(current_widget, 'activate'):
            current_widget.activate(self._previous_index)
        self._previous_index = index

