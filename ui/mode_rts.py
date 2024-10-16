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
    def __init__(self,device):
        super().__init__('Real-Time Spectrum',device)
        
        self.setLayout(self.window_layout)