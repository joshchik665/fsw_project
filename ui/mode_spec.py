from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
)
#from fsw.device import RsFswInstrument
from ui.mode_super import ModeSuper


class ModeSpec(ModeSuper):
    def __init__(self):
        super().__init__('Spectrum')
        
        self.setLayout(self.window_layout)



