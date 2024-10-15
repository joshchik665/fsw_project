from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from fsw.device import RsFswInstrument
from ui.mode_super import ModeSuper

class ModeRts(ModeSuper):
    def __init__(self):
        super().__init__('Real-Time Spectrum')
        
        self.window_layout.addWidget(self.setting_widgets['Center Frequency'])
        
        self.window_layout.addWidget(self.apply_button)
        
        self.setLayout(self.window_layout)