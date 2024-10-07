from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

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
        self.window_layout.addLayout(self.content_layout)
        
        self.instrument = RsFswInstrument.get_instance()
        
        self.mode_index = {
            '0': 'Spectrum',
            '1': 'Real-Time Spectrum Mode',
            '2': 'Zero-Span Mode'
        }
        
        self.mode_scpi_commands = {
            'Spectrum': "SANALYZER",
            'Real-Time Spectrum Mode': "RTIM",
            'Zero-Span Mode': 'SANALYZER',
        }
        
        self.mode = ''
    
    
    def activate(self,previous_index):
        self.instrument.write_str_with_opc(f"INST:CRE:REPL '{self.mode_index[str(previous_index)]}', {self.mode_scpi_commands[self.mode]}, '{self.mode}'")